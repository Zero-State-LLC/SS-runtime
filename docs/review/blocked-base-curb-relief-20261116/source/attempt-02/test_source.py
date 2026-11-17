"""Final bounded correction guards, preserving the first complete source and tests."""
import copy, importlib.util, json, hashlib, os, sys, tempfile, unittest
from pathlib import Path
from unittest.mock import patch
from PIL import Image
HERE=Path(__file__).resolve().parent
SOURCE=HERE.parent
ROOT=SOURCE.parents[3]
def module(name,path):
    spec=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
def load(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
old=module('v9_immutable_first_tests',SOURCE/'test_source.py')
need=old.need

def validate(geometry,registrations=None):
    need(geometry==load(SOURCE/'geometry.json'),'Material correction changed frozen geometry')
    regs=registrations if registrations is not None else load(HERE/'output/registration.json')
    previous=load(SOURCE/'attempt-01/registration.json');need(len(regs)==len(previous)==53,'Fixed53source registrations')
    adjusted=copy.deepcopy(regs)
    for r,p,a in zip(regs,previous,adjusted):
        need({k:v for k,v in r.items() if k!='image'}=={k:v for k,v in p.items() if k!='image'},'Correction changed registration/contact/height/geometry')
        need(r['image']['path']==str((HERE/'output/sprites'/f"{r['id']}.png").relative_to(ROOT)),'Wrong final source path')
        a['image']=p['image']
    return old.validate(geometry,adjusted)

def verify_preview(evidence):
    preview=module('v9_final_preview_tests',HERE/'preview.py');regs=load(HERE/'output/registration.json')
    _,items,ordered,ranks,actors,unknown=preview.scene_inputs(regs)
    need(evidence['attempt']==2 and evidence['nativeEvidence'] is False and evidence['zooms']==[1,1.25,1.4],'Synthetic preview claim drift')
    need(evidence['depthItems']==items and evidence['depthOrder']==ordered['order'] and evidence['depthConstraints']==ordered['constraints'],'Wrong geometry depth evidence')
    need(len(evidence['captures'])==3 and evidence['unknownSilhouetteOverlap'] is False,'Missing preview evidence')
    expected_sources=[dict(name=a['actor']['name'],path=str(a['path'].relative_to(ROOT)),sha256=a['sha256'],actor=a['actor']) for a in actors]
    need(evidence['silhouetteSources']==expected_sources,'Unregistered occlusion mask source')
    for row in evidence['captures']:
        need([x['id'] for x in row['layers']]==[r['id'] for r in sorted(regs,key=lambda r:ranks[r['id']])],'Wrong supplemental preview order')
        for layer in row['layers']:
            need(layer['rank']==ranks[layer['id']] and 0<=layer['visiblePixels']<=layer['rawPixels'],'Visibility count or rank drift')
            for name in layer['occludingActors']:need(name in {a['actor']['name'] for a in actors} and ranks[name]>ranks[layer['id']],'Arbitrary or rear-actor mask')
    return True

def verify_manifest(path=HERE/'manifest.json',replay=False):
    m=load(path);need(m['schema']=='blocked-base-curb-source-009' and m['attempt']==m['maximumAttempts']==2,'Final bounded attempt schema')
    need(m['status']=='FINAL_CORRECTION_PENDING_COORDINATOR' and m['sourceRecommendation'] is None,'Worker cannot recommend')
    required={'author.py','replay.py','preview.py','test_source.py','geometry.json','materials.json','attempt-01-frozen-sha256.json','output/registration.json','output/preview/preview-metadata.json','README.md','ADAPT.md','API.md'}
    need(required<=set(m['files']),'Missing final source dependency')
    for name,digest in m['files'].items():need(sha(old.safe(HERE,name))==digest,'Final source hash drift: '+name)
    frozen=load(HERE/'attempt-01-frozen-sha256.json');need(m['firstAttemptFiles']==frozen,'First attempt freeze changed')
    for name,digest in frozen.items():need(sha(old.safe(ROOT,name))==digest,'First attempt changed: '+name)
    for name,digest in m['baselineFiles'].items():need(sha(old.safe(ROOT,name))==digest,'Retained dependency drift: '+name)
    materials=load(HERE/'materials.json');need(materials['attempt']==materials['maximumAttempts']==2 and materials['geometryChange'] is materials['registrationChange'] is False,'Correction boundary changed')
    need(sha(HERE/'geometry.json')==materials['geometrySHA256']==sha(SOURCE/'geometry.json'),'Exact geometry bytes changed')
    auth=materials['authorization'];need(sha(old.safe(ROOT,auth['path']))==auth['sha256'],'Correction authorization changed')
    regs=load(HERE/'output/registration.json');need(regs==m['sprites'],'Manifest final registrations changed')
    result=validate(load(HERE/'geometry.json'),regs)
    previous=load(SOURCE/'attempt-01/registration.json')
    for r,p in zip(regs,previous):
        file=old.safe(ROOT,r['image']['path']);need(sha(file)==r['image']['sha256'],'Final PNG hash mismatch')
        with Image.open(file) as im,Image.open(ROOT/p['image']['path']) as oldim:
            need(im.mode=='RGBA' and im.size==oldim.size and im.getchannel('A').tobytes()==oldim.getchannel('A').tobytes(),'Material correction changed silhouette/coverage')
    verify_preview(load(HERE/'output/preview/preview-metadata.json'))
    if replay:
        renderer=module('v9_final_replay',HERE/'replay.py')
        with tempfile.TemporaryDirectory(prefix='v9-final-replay-',dir=os.environ.get('JCODE_SCRATCH_DIR')) as tmp:
            out=Path(tmp);renderer.build(out)
            for p in out.rglob('*'):
                if p.is_file():need(p.read_bytes()==(HERE/'output'/p.relative_to(out)).read_bytes(),'Final replay differs: '+p.name)
        result['sourceReplayByteIdentical']=True
    result.update(attempt=2,firstAttemptFilesUnchanged=len(frozen),geometryByteIdentical=True,all53RegistrationAndAlphaIdentical=True)
    return result

class CorrectionTests(unittest.TestCase):
    def test_geometry_and_registration(self):validate(load(HERE/'geometry.json'),load(HERE/'output/registration.json'))
    def test_frozen_source_manifest_and_replay(self):self.assertTrue(verify_manifest(replay=True)['sourceReplayByteIdentical'])
    def test_geometry_mutation(self):
        g=load(HERE/'geometry.json');g['sprites'][0]['heightWorld']=0
        with self.assertRaises(ValueError):validate(g)
    def test_registration_mutations(self):
        for field in ('worldPosition','rootPixelsTopLeft','drawSizeWorld','canvasPixels'):
            r=load(HERE/'output/registration.json');r[0]['registration'][field][0]+=1
            with self.assertRaises(ValueError):validate(load(HERE/'geometry.json'),r)
    def test_contact_height_mutations(self):
        changes=[lambda r:r[0].update(heightWorld=0),lambda r:r[0]['contactWorldXYZ'][0].__setitem__(2,3),lambda r:r[0]['worldBoundsXYZ']['max'].__setitem__(2,50),lambda r:r[0]['geometryLandmarks'][0]['sourcePixelsTopLeft'].__setitem__(0,0)]
        for change in changes:
            r=load(HERE/'output/registration.json');change(r)
            with self.assertRaises(ValueError):validate(load(HERE/'geometry.json'),r)
    def test_no_third_attempt_or_self_recommendation(self):
        for change in [lambda m:m.update(attempt=3),lambda m:m.update(status='recommended'),lambda m:m.update(sourceRecommendation={'decision':'recommended'}),lambda m:m['files'].__setitem__('materials.json','0'*64),lambda m:m['firstAttemptFiles'].__setitem__(next(iter(m['firstAttemptFiles'])),'0'*64)]:
            m=load(HERE/'manifest.json');change(m);real_load=load
            with patch.dict(verify_manifest.__globals__,load=lambda p:m if Path(p)==HERE/'manifest.json' else real_load(p)):
                with self.assertRaises(ValueError):verify_manifest()
    def test_preview_depth_order_mutation(self):
        e=load(HERE/'output/preview/preview-metadata.json');e['depthOrder'].reverse()
        with self.assertRaises(ValueError):verify_preview(e)
    def test_preview_unknown_mask_mutation(self):
        e=load(HERE/'output/preview/preview-metadata.json');e['captures'][0]['layers'][0]['occludingActors'].append('arbitrary-painted-mask')
        with self.assertRaises(ValueError):verify_preview(e)
    def test_preview_rear_mask_mutation(self):
        e=load(HERE/'output/preview/preview-metadata.json');layer=e['captures'][0]['layers'][-1];layer['occludingActors'].append(e['depthOrder'][0])
        with self.assertRaises(ValueError):verify_preview(e)
    def test_preview_source_mutation(self):
        e=load(HERE/'output/preview/preview-metadata.json');e['silhouetteSources'][0]['sha256']='0'*64
        with self.assertRaises(ValueError):verify_preview(e)
    def test_preview_native_claim_mutation(self):
        e=load(HERE/'output/preview/preview-metadata.json');e['nativeEvidence']=True
        with self.assertRaises(ValueError):verify_preview(e)
    def test_preview_replay(self):
        preview=module('v9_final_preview_replay',HERE/'preview.py')
        with tempfile.TemporaryDirectory(prefix='v9-final-preview-replay-',dir=os.environ.get('JCODE_SCRATCH_DIR')) as tmp:
            out=Path(tmp)/'preview';preview.build(out)
            for p in out.iterdir():self.assertEqual(p.read_bytes(),(HERE/'output/preview'/p.name).read_bytes(),p.name)
    def test_overwrite_refused(self):
        renderer=module('v9_final_immutable',HERE/'replay.py')
        with self.assertRaises(RuntimeError):renderer.build(HERE/'output')
if __name__=='__main__':unittest.main(verbosity=2)
