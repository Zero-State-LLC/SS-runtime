"""Independent projection/footprint checks plus active source/export mutations."""
import copy, json, math, os, shutil, subprocess, sys, tempfile, unittest
from pathlib import Path
from PIL import Image
import replay
P=Path(__file__).resolve().parent

def obj_mesh(text):
    mesh={'vertices':[],'faces':[]};uv=[];name='';material=''
    for line in text.splitlines():
        t=line.split()
        if not t:continue
        if t[0]=='v':mesh['vertices'].append([float(x) for x in t[1:]])
        elif t[0]=='vt':uv.append([float(t[1]),1-float(t[2])])
        elif t[0]=='g':name=t[1]
        elif t[0]=='usemtl':material=t[1]
        elif t[0]=='f':
            ids=[tuple(int(x)-1 for x in v.split('/')) for v in t[1:]]
            mesh['faces'].append(dict(name=name,material=material,indices=[v[0] for v in ids],uv=[uv[v[1]] for v in ids]))
    return mesh

class KioskTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.config=replay.load(P/'geometry-controls.json')
        cls.mesh=replay.author(cls.config)
        cls.tex=replay.base.textures(replay.load(P/'materials.json'))
        cls.reg=replay.load(P/'output/registration.json')
        cls.image=replay.render(cls.mesh,cls.tex)

    def test_exact_landmarks(self):
        root=self.reg['rootPixelsTopLeft']
        for record in self.reg['landmarks']:
            x,y,z=record['local']
            expected=[root[0]+5*(x-y)/math.sqrt(2),root[1]-5*((x+y)/(2*math.sqrt(2))+z)]
            for a,b in zip(expected,record['source']):self.assertAlmostEqual(a,b,places=10)
            self.assertEqual(record['world'],[512+x,640+y,z])
        # Independent named, exact canonical ground witnesses.
        points=[[0,0,0],[39,0,0],[128,0,0],[128,128,0],[0,128,0],[0,39,0]]
        for x,y,z in points:
            u,v=replay.base.raw([x,y,z])
            self.assertAlmostEqual(u/5,(x-y)/math.sqrt(2),places=12)
            self.assertAlmostEqual(-v/5,(x+y)/(2*math.sqrt(2)),places=12)

    def test_explicit_ground_boundary(self):
        worlds=[[512,640],[640,640],[640,768],[512,768]]
        self.assertEqual(self.reg['groundBoundaryWorld'],worlds)
        self.assertEqual(len(self.reg['groundPixelsTopLeft']),4)
        for (u,v),(x,y) in zip(self.reg['groundPixelsTopLeft'],worlds):
            self.assertAlmostEqual((u-500)*.2,((x-512)-(y-640))/math.sqrt(2),places=11)
            self.assertAlmostEqual((1160-v)*.2,((x-512)+(y-640))/(2*math.sqrt(2)),places=11)
        self.assertIn('virtual',self.reg['groundBoundaryProvenance'][0])
        self.assertIn('not visible mesh contact',self.reg['groundBoundaryProvenance'][0])

    def test_basis_vectors_and_upright(self):
        a=replay.base.raw([0,0,0]);x=replay.base.raw([1,0,0]);y=replay.base.raw([0,1,0]);z=replay.base.raw([0,0,1])
        self.assertAlmostEqual(x[1]/x[0],-.5)
        self.assertAlmostEqual(y[1]/y[0],.5)
        self.assertEqual(z,(0.0,-5.0))
        self.assertEqual(a,(0.0,-0.0))

    def test_footprint_height_and_chamfer(self):
        for x,y,z in self.mesh['vertices']:
            self.assertGreaterEqual(x,0);self.assertLessEqual(x,128)
            self.assertGreaterEqual(y,0);self.assertLessEqual(y,128)
            self.assertGreaterEqual(x+y,39-1e-10)
            self.assertGreaterEqual(z,0);self.assertLessEqual(z,132)
        self.assertEqual(self.reg['authoritativeBounds'],[512,640,640,768])
        self.assertEqual(self.reg['worldPosition'],[512,640])

    def test_canvas_rederived_uniform_scale(self):
        points=[((x-y)/math.sqrt(2)*5,-((x+y)/(2*math.sqrt(2))+z)*5) for x,y,z in self.mesh['vertices']]+[(0,0)]
        lo=[math.floor(min(p[k] for p in points)/10)*10-40 for k in (0,1)]
        hi=[math.ceil(max(p[k] for p in points)/10)*10+40 for k in (0,1)]
        self.assertEqual(self.reg['canvasPixels'],[hi[k]-lo[k] for k in (0,1)])
        self.assertEqual(self.reg['rootPixelsTopLeft'],[-v for v in lo])
        self.assertEqual(self.reg['drawSizeWorld'],[v*.2 for v in self.reg['canvasPixels']])
        self.assertEqual(self.reg['canvasPixels'],[1000,1200])
        self.assertEqual(self.reg['rootPixelsTopLeft'],[500,1160])

    def test_real_parapet_and_treads(self):
        names={f['name']:f for f in self.mesh['faces']}
        roof=names['recessed-roof']
        self.assertEqual({self.mesh['vertices'][i][2] for i in roof['indices']},{125})
        self.assertEqual(len([n for n in names if n.startswith('parapet-cap')]),5)
        treads=[f for f in self.mesh['faces'] if f['name'].startswith('entry-ledge-') and max(self.mesh['vertices'][i][2] for i in f['indices'])<30]
        self.assertTrue(treads)
        for f in treads:
            vs=[self.mesh['vertices'][i] for i in f['indices']]
            self.assertGreater(replay.base.normal(*vs[:3])[2],0,'Stair tread must face up')
            self.assertEqual(len({v[2] for v in vs}),1)

    def test_uv_bounds_materials_and_output(self):
        for f in self.mesh['faces']:
            self.assertIn(f['material'],self.tex)
            self.assertEqual(len(f['uv']),len(f['indices']))
            for uv in f['uv']:
                self.assertTrue(all(0<=v<=1 for v in uv))
        with Image.open(P/'output/building-alpha.png') as saved:self.assertEqual(saved.tobytes(),self.image.tobytes())
        with Image.open(P/'output/source-full.png') as full:
            self.assertEqual(full.mode,'RGBA');hist=full.getchannel('A').histogram()
            self.assertGreater(hist[0],10000);self.assertGreater(hist[255],10000)
        for name,size in [('native-alpha.png',(200,240)),('half-alpha.png',(100,120))]:
            with Image.open(P/'output'/name) as im:self.assertEqual(im.size,size)

    def test_geometry_mutation_active(self):
        cfg=copy.deepcopy(self.config);cfg['windowRecess']=6.2
        mesh=replay.author(cfg)
        self.assertNotEqual(mesh['vertices'],self.mesh['vertices'])
        changed=replay.render(mesh,self.tex)
        self.assertNotEqual(changed.tobytes(),self.image.tobytes())
        self.assertEqual(replay.base.registration(mesh)['sourceRoot'],self.reg['sourceRoot'])

    def test_uv_mutation_active(self):
        mesh=copy.deepcopy(self.mesh)
        face=next(f for f in mesh['faces'] if f['name']=='south-panel-4-6')
        face['uv']=[[u+.03,v] for u,v in face['uv']]
        changed=replay.render(mesh,self.tex)
        self.assertEqual(mesh['vertices'],self.mesh['vertices'])
        self.assertNotEqual(changed.tobytes(),self.image.tobytes())
        self.assertEqual(changed.getchannel('A').tobytes(),self.image.getchannel('A').tobytes())

    def test_material_mutation_active(self):
        tex=dict(self.tex);tex['facade']=self.tex['door']
        changed=replay.render(self.mesh,tex)
        self.assertNotEqual(changed.tobytes(),self.image.tobytes())
        self.assertEqual(changed.getchannel('A').tobytes(),self.image.getchannel('A').tobytes())

    def test_export_roundtrip_and_actual_obj_mutation(self):
        text=(P/'output/building.obj').read_text();mesh=obj_mesh(text)
        rendered=replay.render(mesh,self.tex)
        self.assertEqual(rendered.tobytes(),self.image.tobytes())
        changed=text.replace(' 132\n',' 140\n')
        self.assertNotEqual(changed,text)
        moved=obj_mesh(changed)
        self.assertNotEqual(replay.base.registration(moved)['sourceCanvas'],self.reg['sourceCanvas'])
        # Actual exported MTL mappings must name the independent atlas-derived files.
        mtl=(P/'output/building.mtl').read_text()
        for name in self.tex:self.assertIn('map_Kd textures/'+name+'.png',mtl)

    def test_manifest_hashes(self):
        manifest=replay.load(P/'output/manifest.json')
        for name,digest in manifest['inputs'].items():self.assertEqual(replay.sha(P/name),digest,name)
        for name,digest in manifest['outputs'].items():self.assertEqual(replay.sha(P/'output'/name),digest,name)

    def test_isolated_replay(self):
        with tempfile.TemporaryDirectory(prefix='kiosk-replay-',dir=os.environ.get('JCODE_SCRATCH_DIR')) as td:
            dest=Path(td)/'packet';dest.mkdir()
            for name in ['replay.py','baseline_renderer.py','geometry-controls.json','materials.json','roof-layer.json']:
                shutil.copy2(P/name,dest/name)
            shutil.copytree(P/'inputs',dest/'inputs')
            run=subprocess.run([sys.executable,str(dest/'replay.py')],cwd=dest,capture_output=True,text=True)
            self.assertEqual(run.returncode,0,run.stderr)
            for name,digest in replay.load(P/'output/manifest.json')['outputs'].items():
                self.assertEqual(replay.sha(dest/'output'/name),digest,name)

if __name__=='__main__':unittest.main(verbosity=2)
