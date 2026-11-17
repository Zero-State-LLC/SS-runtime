"""Adapter tests use explicit in-memory synthetic records, never native evidence."""
import copy
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
from PIL import Image
import native as n


def synthetic(prepared):
    base,old=n.frozen()
    record=copy.deepcopy(old)
    record.update(schema=n.RECORD_SCHEMA,fixtureVersion=n.FIXTURE_VERSION,status=n.STATUS,baselineRecordSHA256=n.BASELINE_SHA,v9InputSHA256=n.V9_INPUT_SHA,sourceManifestSHA256=n.SOURCE_MANIFEST_SHA,harnessSourceReadSHA256=prepared['harnessSourceSHA256'],inputSHA256='a'*64)
    record['loadedTestExecutable']['sha256']='b'*64
    record['captures']=[]
    for arm,zoom in n.ORDER:
        row=copy.deepcopy(next(r for r in old['captures'] if r['arm']=='candidate' and r['zoom']==zoom))
        effective,selected=n.arm_prepared(prepared,arm)
        source=selected['source']
        reg=source['registration']
        row.update(arm=arm,name=f'source-scene-{arm}-ordinary-z{round(zoom*100)}',comparisonRole='CURRENT_FLAT_KIOSK_NATIVE_V9_CONTEXT' if arm=='control' else 'PROPOSED_FLAT_KIOSK_NATIVE_V9_CONTEXT',kioskSourceSHA256=source['sha256'],kioskGeometrySHA256=selected['geometrySHA256'])
        row['buildingSourceSHA256']['benchmark-building']=source['sha256']
        for cohort in ('actors','preprojectionInventory'):
            actor=next(p for p in row[cohort] if p['name']=='benchmark-building')
            actor['size']=reg['drawSizeWorld']
            actor['anchor']=[reg['rootPixelsTopLeft'][0]/reg['canvasPixels'][0],1-reg['rootPixelsTopLeft'][1]/reg['canvasPixels'][1]]
        semantic=dict(row,arm='candidate')
        row['groundFootprints']=n.v9.v7.footprint_expected(semantic,effective)
        row['visibleBuildingContacts']=n.v9.v8.plan_adapter.contact_expected(semantic,effective)
        record['captures'].append(row)
    return record


class NativeAdapterTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.prepared=n.expected_input()
        cls.record=synthetic(cls.prepared)

    def test_synthetic_contract_positive_not_native_proof(self):
        self.assertEqual(len(n.validate_records(self.record,self.prepared,'a'*64)),6)

    def test_current_preparation_exact(self):
        n.validate_prepared(n.load(n.HERE/'prepared/native-inputs.json'),n.HERE/'prepared')
        self.assertEqual(self.prepared,n.load(n.HERE/'prepared/native-inputs.json'))

    def test_all_neighbor_bindings_and_plan_unchanged(self):
        base,_=n.frozen()
        for arm in self.prepared['arms']:
            self.assertEqual([b for b in arm['buildings'] if b['role']!='kiosk'],[b for b in base['buildings'] if b['role']!='kiosk'])
            self.assertEqual([b for b in arm['scenePlan']['buildings'] if b['id']!='solid-03-transit-kiosk'],[b for b in base['scenePlan']['buildings'] if b['id']!='solid-03-transit-kiosk'])
            self.assertEqual(arm['scenePlan']['props'],base['scenePlan']['props'])
            for contact in next(b for b in arm['scenePlan']['buildings'] if b['id']=='solid-03-transit-kiosk')['contactLandmarks']:
                self.assertEqual(contact['sourcePixelsTopLeft'],n.pixel(contact['world'],arm['source']['registration']))

    def test_prepared_neighbor_mutation_rejected(self):
        changed=copy.deepcopy(self.prepared)
        changed['arms'][0]['buildings'][1]['groundPixelsTopLeft'][0][0]+=1
        with self.assertRaisesRegex(ValueError,'binding forged'):n.validate_records(self.record,changed,'a'*64)

    def test_non_kiosk_actor_mutations_rejected(self):
        for name in ['sprite-player','sprite-camera-3','environment-upright-env_solid_01_residential_west','environment-upright-env_solid_02_residential_north','environment-upright-env_solid_04_civic_west','environment-upright-env_solid_05_civic_dais']:
            changed=copy.deepcopy(self.record)
            actor=next(a for a in changed['captures'][0]['actors'] if a['name']==name)
            actor['size'][1]+=1
            with self.assertRaisesRegex(ValueError,'Non-kiosk actor'):n.validate_records(changed,self.prepared,'a'*64)

    def test_depth_ground_field_controls_and_supplements_rejected(self):
        for field in ['depthOrder','depthConstraints','depthItems','groundPlanWitness','cameraRoot','cameraRange','controlsRetained','hudVisible','framing','solids','supplementalActors','supplementalSourceWitnesses']:
            changed=copy.deepcopy(self.record)
            changed['captures'][0][field]=None
            with self.assertRaises(ValueError,msg=field):n.validate_records(changed,self.prepared,'a'*64)

    def test_kiosk_authority_and_wrong_source_rejected(self):
        for field in ['worldRoot','actualZ','depthRank','scale','rotation','size','anchor']:
            changed=copy.deepcopy(self.record)
            actor=next(a for a in changed['captures'][0]['actors'] if a['name']=='benchmark-building')
            actor[field]=[999,999] if isinstance(actor[field],list) else 999
            with self.assertRaises(ValueError,msg=field):n.validate_records(changed,self.prepared,'a'*64)
        for field in ['kioskSourceSHA256','kioskGeometrySHA256']:
            changed=copy.deepcopy(self.record)
            changed['captures'][0][field]='0'*64
            with self.assertRaises(ValueError):n.validate_records(changed,self.prepared,'a'*64)

    def test_missing_capture_extra_fields_and_stale_executable_rejected(self):
        for kind in ['missing','synthetic','acceptance','stale-executable','input','harness']:
            changed=copy.deepcopy(self.record)
            if kind=='missing':changed['captures'].pop()
            if kind=='synthetic':changed['syntheticFixture']=True
            if kind=='acceptance':changed['ownerAcceptance']=True
            if kind=='stale-executable':changed['loadedTestExecutable']=n.frozen()[1]['loadedTestExecutable']
            if kind=='input':changed['inputSHA256']='0'*64
            if kind=='harness':changed['harnessSourceReadSHA256']='0'*64
            with self.assertRaises(ValueError,msg=kind):n.validate_records(changed,self.prepared,'a'*64)

    def test_contact_pixel_and_neighbor_source_mutations_rejected(self):
        for kind in ['contact','footprint','neighbor']:
            changed=copy.deepcopy(self.record)
            row=changed['captures'][0]
            if kind=='contact':row['visibleBuildingContacts'][0]['landmarks'][0]['projectedSource'][0]+=1
            if kind=='footprint':row['groundFootprints'][0]['projectedSource'][0][0]+=1
            if kind=='neighbor':row['buildingSourceSHA256']['environment-upright-env_solid_01_residential_west']='0'*64
            with self.assertRaises(ValueError,msg=kind):n.validate_records(changed,self.prepared,'a'*64)

    def test_exact_test_identity_and_count(self):
        directory=n.V9/'native-capture-v9'
        summary=n.load(directory/'summary.json')
        tree=json.loads(json.dumps(n.load(directory/'tests.json')).replace('BlockedBaseCurbSceneTests','KioskOnlyGeometrySceneTests'))
        n.validate_result(summary,tree)
        with self.assertRaises(ValueError):n.validate_result(summary,n.load(directory/'tests.json'))
        changed=copy.deepcopy(summary)
        changed['passedTests']=0
        with self.assertRaises(ValueError):n.validate_result(changed,tree)

    def test_attachment_identity_and_census(self):
        old=n.load(n.V9/'native-capture-v9/attachment-manifest.json')
        manifest=json.loads(json.dumps(old).replace('BlockedBaseCurbSceneTests','KioskOnlyGeometrySceneTests'))
        n.validate_attachment_manifest(manifest)
        with self.assertRaises(ValueError):n.validate_attachment_manifest(old)
        manifest[0]['attachments'].pop()
        with self.assertRaises(ValueError):n.validate_attachment_manifest(manifest)

    def test_missing_or_symlinked_prepared_fails(self):
        with tempfile.TemporaryDirectory(dir=n.HERE) as temp:
            path=Path(temp)
            with self.assertRaises((ValueError,FileNotFoundError)):n.validate_prepared(self.prepared,path)
            (path/'native-inputs.json').symlink_to(n.HERE/'prepared/native-inputs.json')
            with self.assertRaises(ValueError):n.validate_prepared(self.prepared,path)

    def test_no_preparation_overwrite(self):
        before=n.sha(n.HERE/'prepared/native-inputs.json')
        with self.assertRaises(ValueError):n.prepare()
        self.assertEqual(before,n.sha(n.HERE/'prepared/native-inputs.json'))

    def test_native_pixel_isolation_with_explicit_source_proxy_fixture(self):
        # Source-proxy PNGs exercise the image validator, not native success claims.
        rows=copy.deepcopy(self.record['captures'])
        found={}
        with tempfile.TemporaryDirectory(dir=n.HERE) as temp:
            for row in rows:
                source='current' if row['arm']=='control' else 'proposed'
                path=n.PACKET/f'output/{source}-z{round(row["zoom"]*100)}.png'
                row['pngSHA256']={'-native':n.sha(path)}
                found[row['name']+'-native']=path
            n.verify_images(found,rows)
            original=found[rows[0]['name']+'-native']
            im=Image.open(original).convert('RGB')
            im.putpixel((0,0),(255,0,255))
            changed=Path(temp)/'changed.png'
            im.save(changed)
            found[rows[0]['name']+'-native']=changed
            rows[0]['pngSHA256']['-native']=n.sha(changed)
            with self.assertRaisesRegex(ValueError,'Non-kiosk native pixels'):n.verify_images(found,rows)

    def test_swift_has_only_one_capture_entry_and_all_supplements(self):
        text=(n.ROOT/n.HARNESS).read_text()
        self.assertEqual(text.count('@MainActor func testQuietSouthNeutralOrdinaryScene()'),1)
        self.assertIn('SS_KIOSK_ONLY_GEOMETRY_REVIEW',text)
        self.assertNotIn('arm == "candidate" ? input.supplements',text)
        self.assertNotIn('XCTSkip',text)
        original=(n.ROOT/'AppTests/BlockedBaseCurbSceneTests.swift').read_text()
        self.assertEqual(text[text.index('    @MainActor private func framing('):],original[original.index('    @MainActor private func framing('):])


if __name__=='__main__':unittest.main(verbosity=2)
