"""Portable geometry, registration, immutable input and deterministic replay guards."""
import copy, importlib.util, json, math, os, tempfile, unittest, hashlib
from pathlib import Path
from PIL import Image
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[3]
V8=ROOT/'docs/review/footprint-ground-repair-20261116'
def load(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def need(ok,message):
    if not ok:raise ValueError(message)
def safe(root,name):
    need(isinstance(name,str) and not name.startswith('/') and '\\' not in name and all(v not in ('','.','..') for v in name.split('/')),'Unsafe dependency path')
    p=root/name;need(p.resolve()==p and p.is_file(),'Missing or symlink dependency');return p

def validate(geometry,registrations=None):
    g=geometry;need(g['schema']=='blocked-base-curb-geometry-009' and g['attempt']==1,'Unknown source version/attempt')
    need(g['pixelsPerWorldUnit']==4 and g['paddingPixels']==4 and g['presentationOnly'] is True,'Projection or authority drift')
    need(g['baseEnvelopeWorld']==[512,640,640,768] and g['baseTriangleWorld']==[[512,640],[551,640],[512,679]],'Blocked envelope drift')
    need(g['curbRegionWorld']==[452,572,984,796],'Curb extent drift')
    need(g['props']==load(V8/'plan/plan.json')['props'],'Retained prop roots or base regions drift')
    need(len(g['sprites'])==53 and len({s['id'] for s in g['sprites']})==53,'Supplemental census')
    ids=Image.open(V8/'plan/material-ids.png');px=ids.load();coverage=set();base_count=0
    regs={r['id']:r for r in registrations} if registrations is not None else None
    if regs is not None:need(len(registrations)==53 and set(regs)=={s['id'] for s in g['sprites']},'Registration census')
    for s in g['sprites']:
        root=s['worldPosition'];contact=s['contactLocal'];h=s['heightWorld'];kind=s['kind']
        need(kind in ('blocked-base','curb-relief'),'Unknown source kind')
        need(all(math.isfinite(v) for v in root) and len(root)==2,'Invalid world root')
        world=[[v[0]+root[0],v[1]+root[1],v[2]] for v in contact]
        need(all(v[2]==0 for v in contact),'Floating contact geometry')
        need(all(abs(sum(v[k] for v in contact))<1e-8 for k in (0,1)),'Root must be contact centroid')
        if kind=='blocked-base':
            base_count+=1;need(s['id']=='v9-blocked-kiosk-base' and h==18,'Base vertical height')
            need(world==[[512,640,0],[551,640,0],[512,679,0]],'Exact blocked chamfer triangle coverage')
        else:
            need(h==3 and len(contact)==4,'Curb true relief height')
            x0,y0=world[0][:2];x1,y1=world[2][:2]
            need(world==[[x0,y0,0],[x1,y0,0],[x1,y1,0],[x0,y1,0]],'Curb rectangle contact')
            need(0<x1-x0<=24 and 0<y1-y0<=24,'Small curb pieces only')
            need(all(v*2==int(v*2) for v in (x0,x1,y0,y1)),'Semantic cell alignment')
            for y in range(int(y0*2),int(y1*2)):
                for x in range(int(x0*2),int(x1*2)):
                    need(904<=x<1968 and 1144<=y<1592 and px[x,4607-y]==2,'Relief escaped V8 curb strip')
                    need((x,y) not in coverage,'Overlapping curb geometry');coverage.add((x,y))
        for prop in g['props']:
            xs=[v[0] for v in world];ys=[v[1] for v in world];cx,cy=prop['worldRoot']
            dx=max(min(xs)-cx,0,cx-max(xs));dy=max(min(ys)-cy,0,cy-max(ys))
            need(math.hypot(dx,dy)>prop['contactRadiusWorld'],'Prop base region covered')
        need(len(s['faces'])==len(contact)+1,'Missing cap or vertical wall')
        cap=s['faces'][0];need(cap['normal']==[0,0,1] and cap['vertices']==[[v[0],v[1],h] for v in contact],'Cap geometry mismatch')
        for i,a in enumerate(contact):
            b=contact[(i+1)%len(contact)];f=s['faces'][i+1];dx,dy=b[0]-a[0],b[1]-a[1];length=math.hypot(dx,dy)
            need(f['vertices']==[a,b,[b[0],b[1],h],[a[0],a[1],h]],'Vertical contact-height face mismatch')
            need(all(abs(a-b)<1e-10 for a,b in zip(f['normal'],[dy/length,-dx/length,0])),'Wrong face normal')
        vertices=[v for f in s['faces'] for v in f['vertices']]
        for f in s['faces']:
            need(len(f['uv'])==len(f['vertices']) and all(math.isfinite(n) for uv in f['uv'] for n in uv),'Invalid UV')
            need(f['material'] in ('cap','masonry','curb'),'Material scope')
            for v in f['vertices']:need(all(math.isfinite(n) for n in v) and 0<=v[2]<=h,'Invalid XYZ or height')
        if regs is not None:
            r=regs[s['id']];reg=r['registration'];need(r['kind']==kind and r['heightWorld']==h and r['pixelsPerWorldUnit']==4,'Registration height/kind/scale')
            need(reg['worldPosition']==root and r['contactWorldXYZ']==world,'Actual world contact binding')
            need(r['geometryID']==s['id'] and r['geometryFile']=='geometry.json','Editable geometry binding')
            project=lambda v:((v[0]-v[1])/math.sqrt(2),(v[0]+v[1])/(2*math.sqrt(2))+v[2])
            points=[project(v) for v in vertices]+[(0,0)]
            left=math.floor(min(v[0] for v in points)*4)-4;right=math.ceil(max(v[0] for v in points)*4)+4
            low=math.floor(min(v[1] for v in points)*4)-4;top=math.ceil(max(v[1] for v in points)*4)+4
            need(reg['canvasPixels']==[right-left,top-low] and reg['rootPixelsTopLeft']==[-left,top],'Projection canvas/anchor')
            need(reg['drawSizeWorld']==[(right-left)/4,(top-low)/4],'World draw size drift')
            need(r['worldBoundsXYZ']==dict(min=[min(v[k]+(root[k] if k<2 else 0) for v in vertices) for k in range(3)],max=[max(v[k]+(root[k] if k<2 else 0) for v in vertices) for k in range(3)]),'XYZ bounds drift')
            uniq=sorted(set(tuple(v) for v in vertices));need(len(r['geometryLandmarks'])==len(uniq),'Missing XYZ witnesses')
            for v,w in zip(uniq,r['geometryLandmarks']):
                need(w['worldXYZ']==[v[0]+root[0],v[1]+root[1],v[2]],'World witness drift')
                expected=[-left+4*project(v)[0],top-4*project(v)[1]]
                need(all(abs(a-b)<1e-9 for a,b in zip(expected,w['sourcePixelsTopLeft'])),'D108 XYZ projection mismatch')
            need(r['image']['path']==str((HERE/'attempt-01/sprites'/f"{s['id']}.png").relative_to(ROOT)),'Wrong sprite source path')
    need(base_count==1,'Missing blocked base')
    expected={(x,y) for y in range(1144,1592) for x in range(904,1968) if px[x,4607-y]==2}
    need(coverage==expected,'Incomplete existing curb strip coverage')
    return dict(sprites=53,baseHeight=18,curbHeight=3,curbSemanticPixels=len(coverage),status='SOURCE_GEOMETRY_ONLY_NOT_VISUAL_ACCEPTANCE')

def verify_manifest(path=HERE/'manifest.json',replay=False):
    m=load(path);need(m['schema']=='blocked-base-curb-source-009' and m['attempt']==1,'Unknown manifest')
    need(m['status']=='FIRST_PREVIEW_PENDING_COORDINATOR','Source cannot self-recommend')
    required={'geometry.json','materials.json','author.py','replay.py','preview.py','test_source.py','baseline-sha256.json','ADAPT.md','API.md','attempt-01/registration.json'}
    need(required<=set(m['files']),'Missing editable dependencies')
    for name,digest in m['files'].items():need(sha(safe(HERE,name))==digest,'Source hash drift: '+name)
    need(m['baselineFiles']==load(HERE/'baseline-sha256.json'),'Baseline snapshot mismatch')
    for name,digest in m['baselineFiles'].items():need(sha(safe(ROOT,name))==digest,'V8 or retained dependency changed: '+name)
    regs=load(HERE/'attempt-01/registration.json');need(regs==m['sprites'],'Manifest sprite registration mismatch')
    for r in regs:
        p=safe(ROOT,r['image']['path']);need(sha(p)==r['image']['sha256'],'Sprite hash mismatch')
        with Image.open(p) as im:need(im.mode=='RGBA' and list(im.size)==r['registration']['canvasPixels'] and im.getbbox() is not None,'Sprite image format/canvas')
    result=validate(load(HERE/'geometry.json'),regs)
    if replay:
        spec=importlib.util.spec_from_file_location('v9_replay_proof',HERE/'replay.py');mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
        with tempfile.TemporaryDirectory(prefix='v9-source-replay-',dir=os.environ.get('JCODE_SCRATCH_DIR')) as tmp:
            out=Path(tmp);mod.build(out)
            for p in out.rglob('*'):
                if p.is_file():need(p.read_bytes()==(HERE/'attempt-01'/p.relative_to(out)).read_bytes(),'Deterministic replay differs: '+p.name)
        result['replayByteIdentical']=True
    return result

class SourceTests(unittest.TestCase):
    def setUp(self):self.g=load(HERE/'geometry.json');self.r=load(HERE/'attempt-01/registration.json')
    def test_valid_geometry(self):self.assertEqual(validate(self.g,self.r)['sprites'],53)
    def bad(self,change,regs=False):
        change(self.r if regs else self.g)
        with self.assertRaises(ValueError):validate(self.g,self.r)
    def test_base_flattened(self):self.bad(lambda g:g['sprites'][0].update(heightWorld=0))
    def test_base_root_moved(self):self.bad(lambda g:g['sprites'][0].update(worldPosition=[510,650]))
    def test_base_envelope_widened(self):self.bad(lambda g:g.update(baseEnvelopeWorld=[500,640,640,768]))
    def test_base_contact_missing(self):self.bad(lambda g:g['sprites'][0]['contactLocal'].pop())
    def test_base_vertical_face_missing(self):self.bad(lambda g:g['sprites'][0]['faces'].pop())
    def test_base_height_flattened_in_mesh(self):self.bad(lambda g:g['sprites'][0]['faces'][1]['vertices'][2].__setitem__(2,0))
    def test_curb_off_strip(self):self.bad(lambda g:g['sprites'][1]['worldPosition'].__setitem__(0,700))
    def test_curb_height_lost(self):self.bad(lambda g:g['sprites'][1].update(heightWorld=0))
    def test_curb_missing(self):self.bad(lambda g:g['sprites'].pop())
    def test_curb_duplicates(self):self.bad(lambda g:g['sprites'].__setitem__(2,copy.deepcopy(g['sprites'][1])))
    def test_prop_moved(self):self.bad(lambda g:g['props'][0].update(worldRoot=[525,653]))
    def test_prop_clearance_shrunk(self):self.bad(lambda g:g['props'][0].update(contactRadiusWorld=0))
    def test_anchor_mutation(self):self.bad(lambda r:r[0]['registration']['rootPixelsTopLeft'].__setitem__(0,0),True)
    def test_draw_size_mutation(self):self.bad(lambda r:r[0]['registration']['drawSizeWorld'].__setitem__(0,1),True)
    def test_height_witness_mutation(self):self.bad(lambda r:r[0]['geometryLandmarks'][0]['worldXYZ'].__setitem__(2,9),True)
    def test_projection_mutation(self):self.bad(lambda r:r[0]['geometryLandmarks'][0]['sourcePixelsTopLeft'].__setitem__(0,1),True)
    def test_geometry_bounds_mutation(self):self.bad(lambda r:r[0]['worldBoundsXYZ']['max'].__setitem__(2,0),True)
    def test_wrong_image(self):self.bad(lambda r:r[0]['image'].update(path='../bad.png'),True)
    def test_wrong_normal(self):self.bad(lambda g:g['sprites'][0]['faces'][1].update(normal=[0,0,1]))
    def test_invalid_uv(self):self.bad(lambda g:g['sprites'][0]['faces'][0]['uv'][0].__setitem__(0,float('nan')))
    def test_safe_path(self):
        for name in ('../bad','/bad','foo//bar','./bad'):
            with self.assertRaises(ValueError):safe(HERE,name)
    def test_manifest_and_replay(self):self.assertTrue(verify_manifest(replay=True)['replayByteIdentical'])
    def test_manifest_mutations(self):
        from unittest.mock import patch
        original=load(HERE/'manifest.json')
        changes=[lambda m:m['files'].__setitem__('geometry.json','0'*64),lambda m:m.update(status='recommended'),lambda m:m['files'].pop('materials.json'),lambda m:m['baselineFiles'].__setitem__(next(iter(m['baselineFiles'])),'0'*64),lambda m:m['sprites'][0]['image'].update(sha256='0'*64)]
        real_load=load
        for change in changes:
            mutation=copy.deepcopy(original);change(mutation)
            def altered(p):return mutation if Path(p)==HERE/'manifest.json' else real_load(p)
            with patch.dict(verify_manifest.__globals__,load=altered):
                with self.assertRaises(ValueError):verify_manifest()
    def test_output_overwrite_refused(self):
        spec=importlib.util.spec_from_file_location('v9_immutable_test',HERE/'replay.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
        with self.assertRaises(RuntimeError):m.build(HERE/'attempt-01')
if __name__=='__main__':unittest.main(verbosity=2)
