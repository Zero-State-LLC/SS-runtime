#!/usr/bin/env python3
"""Numerical regression checks, not proof of reference/art fidelity."""
import copy
import json
import math
import unittest

from fit_reference_projection import DEFAULT, fit, inverse, project, report


class ReferenceProjectionFitTests(unittest.TestCase):
    def setUp(self):
        self.data = json.loads(DEFAULT.read_text())

    def test_recovers_known_synthetic_model(self):
        rotation, scale = math.radians(-31), 0.72
        segments = []
        for axis, point in [('east',(1000,0)),('north',(0,1000))]:
            x,y = project(*point,rotation,scale)
            for index in range(2):
                segments.append(dict(axis=axis,use='fit',start=[index*20,10],end=[x+index*20,10-y]))
        r,k,_ = fit(segments)
        self.assertAlmostEqual(r,rotation,places=12)
        self.assertAlmostEqual(k,scale,places=12)

    def test_holdouts_do_not_train_fit(self):
        original = fit(self.data['segments'])
        altered = copy.deepcopy(self.data['segments'])
        for row in altered:
            if row['use']=='holdout':
                row['end']=[row['start'][0]+20,row['start'][1]+30]
        self.assertEqual(original,fit(altered))

    def test_inverse_preserves_vectors_not_screen_speed(self):
        for rotation,scale in [(math.pi/4,.5),fit(self.data['segments'])[:2]]:
            for x,y in [(1,0),(1,1),(0,1),(-1,1),(-1,0),(-1,-1),(0,-1),(1,-1)]:
                for magnitude in (.25,.5,1,120):
                    unit=math.hypot(x,y)
                    point=(x/unit*magnitude,y/unit*magnitude)
                    result=inverse(*project(*point,rotation,scale),rotation,scale)
                    self.assertAlmostEqual(result[0],point[0],places=10)
                    self.assertAlmostEqual(result[1],point[1],places=10)
        self.assertAlmostEqual(math.hypot(*project(2**-.5,2**-.5,math.pi/4,.5)),.5)
        self.assertAlmostEqual(math.hypot(*project(2**-.5,-2**-.5,math.pi/4,.5)),1)

    def test_invalid_observations_fail(self):
        for end in ([312,666],[float('nan'),3],[311,700],[500,666]):
            segments=copy.deepcopy(self.data['segments'])
            segments[0]['end']=end
            with self.assertRaises(ValueError):
                fit(segments)
        with self.assertRaises(ValueError):
            fit(self.data['segments'][:2])

    def test_report_is_reproducible_and_keeps_uncertainty(self):
        result=report(DEFAULT)
        self.assertEqual(result,report(DEFAULT))
        self.assertEqual(result,json.loads((DEFAULT.parent/'ground-fit.json').read_text()))
        self.assertGreater(max(abs(r['residualDegrees']) for r in result['residuals']),2)
        self.assertLess(result['sensitivity']['yScale'][0],1)
        self.assertGreater(result['sensitivity']['yScale'][1],1)
        self.assertEqual(result['offlineRoundTrips'],32)
        self.assertEqual(len(result['referenceSHA256']),64)


if __name__=='__main__':
    unittest.main()
