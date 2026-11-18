"""Portable V9 protocol/negative tests. Synthetic data never becomes native evidence."""
import copy
import importlib.util
import json
import os
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
from PIL import Image

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location('_v9_tests_native', HERE/'native.py')
n = importlib.util.module_from_spec(spec)
spec.loader.exec_module(n)
b = n.supplement_adapter


def source_geometry():
    geometry = n.load(b.SOURCE/'geometry.json')
    sprites = n.load(b.SOURCE/'output/registration.json')
    props = n.load(b.V8/'plan/plan.json')['props']
    with Image.open(b.V8/'plan/material-ids.png') as image:
        normalized = b.validate_geometry(geometry, sprites, image, props)
    return geometry, sprites, props, normalized


def synthetic():
    old = n.baseline()
    prior = n.load(n.V8/'native-inputs-v8/native-inputs.json')
    normalized = source_geometry()[3]
    prepared = copy.deepcopy(prior)
    prepared.update(schema=n.INPUT_SCHEMA,fixtureVersion=n.FIXTURE_VERSION,assemblySHA256='a'*64,
                    harnessSourceSHA256=n.sha(n.ROOT/n.HARNESS),baselineRecordSHA256=n.BASELINE_SHA,
                    supplements=normalized,supplementalManifestSHA256='b'*64,
                    supplementalBinding={'manifest':{'sha256':'b'*64},'SYNTHETIC_ONLY':True})
    record = {k:copy.deepcopy(v) for k,v in old.items() if k != 'captures'}
    record.update(schema=n.RECORD_SCHEMA,fixtureVersion=n.FIXTURE_VERSION,assemblySHA256=prepared['assemblySHA256'],
                  inputSHA256='SYNTHETIC_NOT_NATIVE',harnessSourceReadSHA256=prepared['harnessSourceSHA256'],
                  baselineRecordSHA256=n.BASELINE_SHA,supplementalManifestSHA256='b'*64,
                  loadedTestExecutable=dict(path='/SYNTHETIC/SSRuntimeTests.xctest/SSRuntimeTests',sha256='c'*64),captures=[])
    for arm,zoom in n.ORDER:
        row=copy.deepcopy(next(c for c in old['captures'] if c['arm']=='candidate' and c['zoom']==zoom))
        row.update(arm=arm,name=f'source-scene-{arm}-ordinary-z{round(zoom*100)}',
                   comparisonRole='BASELINE_V8_CANDIDATE' if arm=='control' else 'CANDIDATE_V9_BASE_CURB_RELIEF',
                   supplementalActors=[],supplementalSourceWitnesses=[],supplementalCount=0,totalPresentationUprightCount=18)
        supplements=normalized if arm=='candidate' else []
        for item in supplements:
            actor,witness=n.supplemental_expected(item,row)
            row['supplementalActors'].append(actor)
            row['supplementalSourceWitnesses'].append(witness)
        row['supplementalCount']=len(supplements)
        row['totalPresentationUprightCount']=18+len(supplements)
        if supplements:
            items=n.v5.expected_depth_items(row,n.CENTER)
            items += [dict(name=s['nodeName'],worldRoot=s['registration']['worldPosition'],footprint=s['footprintWorld'],projectedRootY=n.a.project(s['registration']['worldPosition'])[1]) for s in supplements]
            order=n.v5.depth_order(items)
            row.update(depthItems=items,depthOrder=order['order'],depthConstraints=order['constraints'])
            actors=row['actors']+row['supplementalActors']
            for actor in actors:
                rank=order['order'].index(actor['name'])
                actor.update(depthRank=rank,actualZ=row['depthBase']+rank/len(actors)*.5)
        record['captures'].append(row)
    return record,prepared,prior,dict(supplements=copy.deepcopy(normalized))


class Records(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.fixture=synthetic()

    def setUp(self):
        self.record,self.prepared,self.prior,self.normalized=copy.deepcopy(self.fixture)

    def validate(self):
        with patch.object(n.v8,'expected_input',return_value=self.prior),patch.object(n.supplement_adapter,'validate',return_value=self.normalized):
            return n.validate_records(self.record,self.prepared,'SYNTHETIC_NOT_NATIVE')

    def test_synthetic_protocol_only(self):
        self.assertEqual(len(self.validate()),6)
        self.assertEqual(self.record['captures'][3]['uprightCount'],18)
        self.assertEqual(self.record['captures'][3]['supplementalCount'],53)

    def test_each_frozen_v8_field_rejects(self):
        row=self.record['captures'][3]
        mutable={'arm','name','comparisonRole','pngSHA256','nativePixels','actors','depthOrder','depthItems','depthConstraints'}
        previous=n.baseline()['captures'][3]
        for key in previous.keys()-mutable:
            with self.subTest(key=key):
                old=row[key];row[key]=None
                with self.assertRaises((ValueError,TypeError,KeyError)):self.validate()
                row[key]=old

    def test_every_old_actor_field_rejects(self):
        for actor in self.record['captures'][3]['actors']:
            for key in actor:
                with self.subTest(actor=actor['name'],key=key):
                    old=actor[key];actor[key]=None
                    with self.assertRaises((ValueError,TypeError,KeyError)):self.validate()
                    actor[key]=old

    def test_every_supplement_registration_field_rejects(self):
        actor=self.record['captures'][3]['supplementalActors'][0]
        for key in actor:
            with self.subTest(key=key):
                old=actor[key];actor[key]=None
                with self.assertRaises((ValueError,TypeError,KeyError)):self.validate()
                actor[key]=old

    def test_each_xyz_witness_field_rejects(self):
        witness=self.record['captures'][3]['supplementalSourceWitnesses'][0]
        for obj in (witness,witness['vertices'][0]):
            for key in obj:
                with self.subTest(key=key):
                    old=obj[key];obj[key]=None
                    with self.assertRaises((ValueError,TypeError,KeyError)):self.validate()
                    obj[key]=old

    def test_supplement_not_old_actor(self):
        row=self.record['captures'][3]
        row['actors'].append(row['supplementalActors'].pop())
        with self.assertRaises(ValueError):self.validate()

    def test_no_baseline_supplement(self):
        self.record['captures'][0]['supplementalActors']=self.record['captures'][3]['supplementalActors']
        with self.assertRaises(ValueError):self.validate()

    def test_no_rank_boost(self):
        row=self.record['captures'][3]
        row['supplementalActors'][0]['actualZ']+=1
        with self.assertRaises(ValueError):self.validate()

    def test_depth_constraint_tamper(self):
        for key in ('depthItems','depthOrder','depthConstraints'):
            row=self.record['captures'][3];old=row[key];row[key]=[]
            with self.assertRaises(ValueError):self.validate()
            row[key]=old

    def test_exact_float_ground_oracle(self):
        self.record['captures'][3]['groundPlanWitness']['zPosition']=.1
        with self.assertRaises(ValueError):self.validate()

    def test_old_plan_source_and_authority_preserved(self):
        for key in ('sources','scenePlan','planBinding','buildings','planSHA256'):
            old=self.prepared[key];self.prepared[key]=None
            with self.assertRaises(ValueError):self.validate()
            self.prepared[key]=old

    def test_forged_supplement_geometry(self):
        self.prepared['supplements'][0]['verticesWorldXYZ'][0][0]+=1
        with self.assertRaises(ValueError):self.validate()

    def test_wrong_capture_count_or_arm(self):
        self.record['captures'][0]=copy.deepcopy(self.record['captures'][1])
        with self.assertRaises(ValueError):self.validate()

    def test_old_binary_fails(self):
        self.record['loadedTestExecutable']=n.baseline()['loadedTestExecutable']
        with self.assertRaises(ValueError):self.validate()

    def test_stale_sources_or_input(self):
        for key in ('inputSHA256','assemblySHA256','harnessSourceReadSHA256','supplementalManifestSHA256','planSHA256'):
            old=self.record[key];self.record[key]='f'*64
            with self.assertRaises(ValueError):self.validate()
            self.record[key]=old

    def test_synthetic_claim_rejected(self):
        self.record['syntheticFixture']=True
        with self.assertRaises(ValueError):self.validate()

    def test_one_passed_test_required(self):
        summary=dict(result='Passed',passedTests=1,totalTestCount=1,failedTests=0,skippedTests=0,expectedFailures=0)
        tree=dict(testNodes=[dict(nodeType='Test Case',nodeIdentifier=n.TEST,result='Passed')])
        n.validate_result(summary,tree)
        for key in ('passedTests','totalTestCount','failedTests','skippedTests','expectedFailures'):
            bad=copy.deepcopy(summary);bad[key]+=1
            with self.assertRaises(ValueError):n.validate_result(bad,tree)
        tree['testNodes'][0]['nodeIdentifier']=n.v8.TEST
        with self.assertRaises(ValueError):n.validate_result(summary,tree)

    def test_actual_executable_bytes_required(self):
        with tempfile.TemporaryDirectory(dir=os.environ.get('JCODE_SCRATCH_DIR')) as temp:
            binary=Path(temp)/'SSRuntimeTests';binary.write_bytes(b'SYNTHETIC NOT NATIVE')
            with self.assertRaises(ValueError):n.validate_executable(self.record,binary)
            self.record['loadedTestExecutable']['sha256']=n.sha(binary)
            n.validate_executable(self.record,binary)
            binary.write_bytes(b'changed')
            with self.assertRaises(ValueError):n.validate_executable(self.record,binary)


class Geometry(unittest.TestCase):
    def setUp(self):
        self.geometry,self.sprites,self.props,_=source_geometry()
        self.ids=Image.open(b.V8/'plan/material-ids.png')
        self.addCleanup(self.ids.close)

    def validate(self):return b.validate_geometry(self.geometry,self.sprites,self.ids,self.props)

    def test_real_source_geometry_without_recommendation(self):self.assertEqual(len(self.validate()),53)

    def test_escape_blocked_corner(self):
        self.geometry['sprites'][0]['contactLocal'][0][0]-=1
        with self.assertRaises(ValueError):self.validate()

    def test_flat_ground_patch_rejected(self):
        self.geometry['sprites'][0]['heightWorld']=0
        with self.assertRaises(ValueError):self.validate()

    def test_unbound_height_and_landmark_rejected(self):
        for key in ('heightWorld','geometryLandmarks','worldBoundsXYZ','contactWorldXYZ'):
            old=self.sprites[0][key];self.sprites[0][key]=None
            with self.assertRaises((ValueError,TypeError)):self.validate()
            self.sprites[0][key]=old

    def test_unauthorized_extra_mesh_vertex(self):
        self.geometry['sprites'][0]['faces'][0]['vertices'][0][0]-=100
        with self.assertRaises(ValueError):self.validate()

    def test_curb_semantic_boundary_change(self):
        sprite=self.sprites[1];x,y,_=sprite['contactWorldXYZ'][0]
        self.ids.putpixel((int(x*2),4607-int(y*2)),1)
        with self.assertRaises(ValueError):self.validate()

    def test_no_missing_or_duplicate_supplement(self):
        self.sprites.pop()
        with self.assertRaises(ValueError):self.validate()

    def test_prop_contact_region_protected(self):
        self.geometry['props'][0]['worldRoot']=self.sprites[1]['registration']['worldPosition']
        self.props=self.geometry['props']
        with self.assertRaises(ValueError):self.validate()

    def test_no_third_attempt(self):
        self.geometry['attempt']=3
        with self.assertRaises(ValueError):self.validate()

    def test_paths_and_symlinks(self):
        for value in ('../escape','/absolute','x//y','x/../y','x\\y'):
            with self.assertRaises(ValueError):b.dependency(dict(path=value,sha256='a'*64),n.ROOT)
        with tempfile.TemporaryDirectory(dir=os.environ.get('JCODE_SCRATCH_DIR')) as temp:
            root=Path(temp);(root/'target').write_bytes(b'x');(root/'link').symlink_to(root/'target')
            with self.assertRaises(ValueError):b.dependency(dict(path='link',sha256=b.sha(root/'target')),root)


class Evidence(unittest.TestCase):
    def test_prepared_old_and_new_source_symlinks_rejected(self):
        with tempfile.TemporaryDirectory(dir=os.environ.get('JCODE_SCRATCH_DIR')) as temp:
            root=Path(temp).resolve()
            (root/'native-inputs.json').write_text('{}')
            (root/'target.png').write_bytes(b'SYNTHETIC')
            (root/'alias.png').symlink_to(root/'target.png')
            source=dict(file='alias.png',sha256=n.sha(root/'target.png'))
            for cohort in ('sources','supplements'):
                prepared=dict(sources=[],supplements=[]);prepared[cohort]=[source]
                with self.assertRaises(ValueError):n.validate_prepared_files(prepared,root)

    def test_each_unchanged_v8_assembly_key_rejects(self):
        old=n.load(n.V8/'assembly.json')
        manifest=copy.deepcopy(old)
        manifest.update(schema='blocked-base-curb-assembly-009',fixtureVersion=n.FIXTURE_VERSION,baselineRecordSHA256=n.BASELINE_SHA,supplementalBinding={},supplements=[])
        for key in set(old)-{'schema','fixtureVersion','baselineRecordSHA256'}:
            bad=copy.deepcopy(manifest);bad[key]=None
            with self.subTest(key=key),self.assertRaises(ValueError):n.validate_manifest(bad)

    def test_old_native_packet_not_v9_evidence(self):
        retained=n.import_path('_v9_retained_negative',HERE/'retained.py')
        with self.assertRaises(ValueError):retained.verify(n.BASELINE_CAPTURE,n.V8/'native-inputs-v8')

    def test_pending_no_outputs(self):
        with tempfile.TemporaryDirectory(dir=os.environ.get('JCODE_SCRATCH_DIR')) as temp:
            root=Path(temp);rec=root/'rec.json';rec.write_text('{}')
            with self.assertRaises(ValueError):n.bind(rec,root/'assembly.json')
            self.assertFalse((root/'assembly.json').exists())
            with self.assertRaises(FileNotFoundError):n.prepare(manifest=root/'missing.json',output=root/'inputs')
            self.assertFalse((root/'inputs').exists())

    def test_nine_complete_rgba_baselines(self):
        found={row['name'].replace('-candidate-','-control-')+suffix:n.BASELINE_CAPTURE/(row['name']+suffix+'.png') for row in n.baseline()['captures'][3:] for suffix in row['pngSHA256']}
        n.baseline_pixels(found)
        with tempfile.TemporaryDirectory(dir=os.environ.get('JCODE_SCRATCH_DIR')) as temp:
            for key in sorted(found):
                original=found[key];changed=Path(temp)/(key+'.png')
                with Image.open(original) as source:
                    image=source.convert('RGBA');rgba=image.getpixel((0,0));image.putpixel((0,0),((rgba[0]+1)%256,*rgba[1:]));image.save(changed)
                found[key]=changed
                with self.assertRaises(ValueError):n.baseline_pixels(found)
                found[key]=original

    def test_current_v8_source_harness_float_guard_retained(self):
        text=(n.ROOT/n.HARNESS).read_text()
        self.assertIn('patch.zPosition == CGFloat(Float(0.1))',text)
        self.assertIn('Bundle(for: Self.self).executableURL',text)
        self.assertIn('supplementalSourceWitnesses',text)
        self.assertNotIn('XCTSkip',text)


if __name__=='__main__':unittest.main()
