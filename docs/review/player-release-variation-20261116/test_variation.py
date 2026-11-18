#!/usr/bin/env python3
"""Portable real-source geometry regressions, no rendering or native claims."""
import copy
import hashlib
import json
import math
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
import variation as v

class SourceVariationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.sources,cls.neutral,cls.samples,cls.facts=v.expected(v.BASE/'fixtures')

    def test_zero_variation_exact_baseline(self):
        for p in v.NEW:
            got=v.generate(self.sources[p-1],self.neutral,p,0)
            original=v.load(v.BASE/'artifacts'/f'phase-{p:02d}/samples.json')
            self.assertEqual(got,original)
            self.assertEqual(json.dumps(got,indent=2,allow_nan=False)+'\n',(v.BASE/'artifacts'/f'phase-{p:02d}/samples.json').read_text())

    def test_repeatable_without_input_mutation(self):
        before=copy.deepcopy(self.sources)
        for p in v.NEW:
            self.assertEqual(self.samples[p],v.generate(self.sources[p-1],self.neutral,p))
        self.assertEqual(self.sources,before)

    def test_each_phase_has_changed_intermediate_geometry(self):
        for p in v.NEW:
            baseline=v.b.generate(self.sources[p-1],self.neutral)
            self.assertTrue(any(self.samples[p][k]['legs']!=baseline[k]['legs'] for k in range(2,16)))

    def test_phase_specific_not_same_trajectory(self):
        # Same starting source with two different phase indices isolates the profile effect.
        a=v.generate(self.sources[0],self.neutral,1)
        b=v.generate(self.sources[0],self.neutral,2)
        self.assertNotEqual(a[4]['legs'],b[4]['legs'])
        self.assertNotEqual(a[12]['legs'],b[12]['legs'])

    def test_profile_uses_actual_source_stance(self):
        source=copy.deepcopy(self.sources[0]);altered=copy.deepcopy(source)
        v.b.legs(altered)['left']['toe'][2]+=1
        self.assertNotEqual(v.profile(source,1),v.profile(altered,1))
        for p in v.NEW:
            self.assertEqual(v.profile(self.sources[p-1],p)['support'],v.b.support_side(self.sources[p-1]))

    def test_preserved_samples_exact(self):
        for p in v.b.PRESERVED:
            self.assertEqual(self.samples[p],v.load(v.BASE/'artifacts'/f'phase-{p:02d}/samples.json'))
            with self.assertRaisesRegex(ValueError,'cannot be regenerated'):
                v.generate(self.sources[p-1],self.neutral,p)

    def test_exact_entry_and_neutral_geometry(self):
        for p in v.NEW:
            self.assertEqual(self.samples[p][0]['legs'],self.sources[p-1]['legs'])
            for side,leg in v.b.legs(self.samples[p][-1]).items():
                for key in ('hip','knee','ankle','heel','toe'):
                    self.assertTrue(v.b.np.allclose(leg[key],v.b.legs(self.neutral)[side][key],rtol=0,atol=v.b.EPS))

    def test_exact_timing_order(self):
        for p in v.NEW:
            self.assertEqual([s['settleSeconds'] for s in self.samples[p]],[k*3/128 for k in range(17)])
            self.assertEqual([s['settleProgress'] for s in self.samples[p]],[k/16 for k in range(17)])
        self.assertEqual(v.b.TIMING['neutralBoundarySeconds'],0.375)

    def test_continuous_easing_monotonic_and_bounded(self):
        # e(t)=smooth(g(t)), g=t+a*t*(1-t). g'>=1-|a|>=.88.
        # smooth'=6*g*(1-g)>=0 on[0,1]. Polynomial composition is continuous/C1.
        for skew in [-.12,0,.12]+[v.profile(self.sources[p-1],p)['transferSkew'] for p in v.NEW]:
            values=[v.ease(k/1000,skew) for k in range(1001)]
            self.assertEqual((values[0],values[-1]),(0,1))
            self.assertTrue(all(a<=b for a,b in zip(values,values[1:])))
            for k in range(1001):
                t=k/1000;g=t+skew*t*(1-t)
                self.assertGreaterEqual(1+skew*(1-2*t),.88)
                self.assertGreaterEqual(6*g*(1-g)*(1+skew*(1-2*t)),-1e-14)

    def test_profile_limits_are_proposal_domain(self):
        for p in v.NEW:
            profile=v.profile(self.sources[p-1],p)
            self.assertLessEqual(abs(profile['transferSkew']),.12)
            self.assertLessEqual(abs(profile['recoverySkew']),.12)
            self.assertTrue(2.75<=profile['lift']<=3.25)
        for invalid in (-.1,1.1,math.nan,math.inf):
            with self.assertRaises(ValueError):v.profile(self.sources[0],1,invalid)
        for t,skew in ((-.1,0),(1.1,0),(.5,.121),(math.nan,0),(.5,math.inf)):
            with self.assertRaises(ValueError):v.ease(t,skew)

    def test_all_geometry_and_contacts(self):
        self.assertEqual(sum(len(f['measurements']) for f in self.facts),544)
        for f in self.facts:
            self.assertEqual(f['simultaneousHorizontalToeMoves'],[])
            self.assertTrue(all(c['maximumToeDrift']==0 for c in f['contactIntervals']))

    def test_contact_intervals_identical_to_baseline(self):
        for p in v.NEW:
            baseline=v.b.validate(v.b.generate(self.sources[p-1],self.neutral),self.sources[p-1],self.neutral,p)
            self.assertEqual(self.facts[p-1]['contactIntervals'],baseline['contactIntervals'])

    def test_reject_contact_slide(self):
        samples=copy.deepcopy(self.samples[1]);leg=v.b.legs(samples[3])['right']
        # Translate full leg so lengths remain valid, isolating contact drift.
        for key in ('hip','knee','ankle','heel','toe','contactWorld'):leg[key][0]+=.1
        with self.assertRaisesRegex(ValueError,'drift'):v.b.validate(samples,self.sources[0],self.neutral,1)

    def test_reject_limb_tamper(self):
        samples=copy.deepcopy(self.samples[1]);samples[3]['legs'][0]['knee'][0]+=.1
        with self.assertRaisesRegex(ValueError,'segment lengths'):v.b.validate(samples,self.sources[0],self.neutral,1)

    def test_reject_contact_schedule_tamper(self):
        samples=copy.deepcopy(self.samples[1]);v.b.legs(samples[10])['right']['contact']=True
        with self.assertRaisesRegex(ValueError,'contact schedule'):v.b.validate(samples,self.sources[0],self.neutral,1)

    def test_reject_order_tamper(self):
        samples=copy.deepcopy(self.samples[1]);samples[3],samples[4]=samples[4],samples[3]
        with self.assertRaisesRegex(ValueError,'sample order'):v.b.validate(samples,self.sources[0],self.neutral,1)

    def test_locked_baseline(self):
        self.assertEqual(v.provenance(),v.load(v.HERE/'baseline-lock.json'))
        with patch.object(v.b,'sha',return_value='0'*64):
            with self.assertRaisesRegex(ValueError,'lock mismatch'):v.provenance()

    def test_batch_rejects_unbounded_or_preserved(self):
        for phases in ([],[1,2,3],[5],[13],[1,1],[0],[17]):
            with self.assertRaisesRegex(ValueError,'Batches must'):v.batch(Path('.'),Path('.'),phases)

    def test_incomplete_checkpoint_fails_closed(self):
        with tempfile.TemporaryDirectory(dir=v.HERE) as directory:
            self.assertFalse(v.b.completed_work(v.BASE/'fixtures',Path(directory),self.samples[1]))

if __name__=='__main__':unittest.main(verbosity=2)
