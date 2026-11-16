"""Focused real-source checks, not runtime or visual acceptance."""
import copy
import math
import shutil
import subprocess
import sys
import tempfile
import unittest
from collections import Counter
from pathlib import Path
from PIL import Image, ImageChops, ImageDraw, ImageFilter
import replay
P=Path(__file__).resolve().parent

class SourceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.mesh=replay.load(P/'mesh.json')
        cls.spec=replay.load(P/'materials.json')
        cls.tex=replay.textures(cls.spec)
        cls.reg=replay.registration(cls.mesh)
        cls.image=replay.render(cls.mesh,cls.tex)

    def test_exact_inputs_and_explicit_crops(self):
        manifest=replay.load(P/'output/manifest.json')
        for name,digest in manifest['inputs'].items():
            self.assertEqual(replay.sha(P/name),digest,name)
        self.assertEqual(replay.sha(P/'inputs/benchmark.png'),'49aa35447230187e3eabe948cdc8eba6d6d465b2605d624e2cf7443f6cb69ffb')
        self.assertEqual(self.spec['rects'],{'facade':[29,120,552,894],'door':[594,120,914,894],'roof':[956,248,1508,796]})
        with Image.open(P/'inputs/atlas.png') as atlas:
            self.assertEqual(atlas.size,(1536,1024))
            for name,rect in self.spec['rects'].items():
                self.assertEqual(self.tex[name].tobytes(),atlas.crop(rect).convert('RGBA').tobytes())

    def test_closed_oriented_mesh(self):
        edges=Counter()
        for face in self.mesh['faces']:
            ids=face['indices']
            self.assertEqual(len(ids),len(face['uv']))
            self.assertGreater(sum(v*v for v in replay.normal(*(self.mesh['vertices'][i] for i in ids[:3]))),0)
            for a,b in zip(ids,ids[1:]+ids[:1]): edges[a,b]+=1
        for (a,b),count in edges.items():
            self.assertEqual(count,1)
            self.assertEqual(edges[b,a],1)
        self.assertEqual(len(self.mesh['vertices'])-len(edges)//2+len(self.mesh['faces']),2)
        self.assertEqual(len(self.mesh['vertices']),10)
        self.assertEqual(len(self.mesh['faces']),7)

    def test_uv_is_explicit_upright_unmirrored_reuse(self):
        for face in self.mesh['faces'][:5]:
            self.assertEqual(face['uv'],[[0,1],[1,1],[1,0],[0,0]])
            vertices=[self.mesh['vertices'][i] for i in face['indices']]
            self.assertEqual([v[2] for v in vertices],[0,0,132,132])
        self.assertEqual([f['material'] for f in self.mesh['faces'][:5]],['facade']*4+['door'])
        self.assertEqual({f['name'] for f in self.mesh['faces'] if f['hidden']},{'hidden-east','hidden-north','floor'})

    def test_actual_proportions_contact_and_collision(self):
        v=self.mesh['vertices']
        side=math.dist(v[0],v[1])
        door=math.dist(v[4],v[0])
        self.assertEqual(side,89)
        self.assertAlmostEqual(side/132,524/774,delta=.004)
        self.assertAlmostEqual(door/132,320/774,delta=.005)
        self.assertEqual(min(p[2] for p in v),0)
        self.assertEqual(max(p[2] for p in v),132)
        self.assertEqual(self.reg['authoritativeBounds'],[512,640,640,768])
        self.assertEqual(self.reg['worldRoot'],[512,640,0])
        self.assertTrue(all(0<=p[0]<=128 and 0<=p[1]<=128 for p in v))

    def test_registration_independently_projected(self):
        reg=replay.load(P/'output/registration.json')
        self.assertEqual(reg,self.reg)
        w,h=reg['sourceCanvas']
        ru,rv=reg['sourceRoot']
        self.assertNotEqual(reg['sourceRoot'],[560,885])
        self.assertEqual(reg['sourcePixelsPerWorldUnit'],5)
        self.assertEqual(reg['uniformDrawScale'],.2)
        self.assertEqual(reg['spriteSizeScenePoints'],[w/5,h/5])
        self.assertEqual(reg['spriteAnchorBottomLeft'],[ru/w,1-rv/h])
        for point in reg['landmarks']:
            x,y,z=point['local']
            expected=[ru+5*(x-y)/math.sqrt(2),rv-5*((x+y)/(2*math.sqrt(2))+z)]
            for actual,want in zip(point['source'],expected): self.assertAlmostEqual(actual,want)
            self.assertEqual(point['world'],[512+x,640+y,z])
            self.assertTrue(0<expected[0]<w and 0<expected[1]<h)
        self.assertFalse(reg['ownerAccepted'])
        self.assertFalse(reg['productionAdmitted'])

    def test_alpha_bounds_and_no_interior_holes(self):
        alpha=self.image.getchannel('A')
        x0,y0,x1,y1=alpha.getbbox()
        self.assertGreaterEqual(min(x0,y0),30)
        self.assertLess(x1,self.image.width-30)
        self.assertLess(y1,self.image.height-30)
        mask=Image.new('L',self.image.size)
        draw=ImageDraw.Draw(mask)
        root=self.reg['sourceRoot']
        for face in self.mesh['faces']:
            verts=[self.mesh['vertices'][i] for i in face['indices']]
            n=replay.normal(*verts[:3])
            if -n[0]-n[1]+n[2]<=0: continue
            draw.polygon([tuple(replay.raw(v)[k]+root[k] for k in (0,1)) for v in verts],fill=255)
        interior=mask.filter(ImageFilter.MinFilter(5))
        self.assertIsNone(ImageChops.subtract(interior,alpha).getbbox())
        self.assertEqual(alpha.getpixel((0,0)),0)
        self.assertEqual(alpha.getpixel((self.image.width-1,self.image.height-1)),0)

    def test_no_magenta_contamination(self):
        for name,image in list(self.tex.items())+[('render',self.image)]:
            colors=image.getdata()
            self.assertFalse(any(a>0 and r>180 and b>180 and g<100 for r,g,b,a in colors),name)

    def test_mesh_mutation_changes_render_and_registration(self):
        changed=copy.deepcopy(self.mesh)
        for v in changed['vertices'][5:]: v[2]+=12
        result=replay.render(changed,self.tex)
        self.assertNotEqual(self.image.size,result.size)
        self.assertNotEqual(self.reg['sourceRoot'],replay.registration(changed)['sourceRoot'])
        # A local lateral geometry edit changes pixels without altering texture bytes.
        changed=copy.deepcopy(self.mesh)
        changed['vertices'][0][0]+=8
        changed['vertices'][5][0]+=8
        self.assertNotEqual(replay.render(changed,self.tex).tobytes(),self.image.tobytes())

    def test_uv_mutation_changes_pixels_not_geometry(self):
        changed=copy.deepcopy(self.mesh)
        changed['faces'][0]['uv']=[[.15,1],[.85,1],[.85,0],[.15,0]]
        result=replay.render(changed,self.tex)
        self.assertEqual(replay.registration(changed),self.reg)
        self.assertNotEqual(result.tobytes(),self.image.tobytes())
        self.assertEqual(result.getchannel('A').tobytes(),self.image.getchannel('A').tobytes())

    def test_each_material_mutation_changes_visible_pixels(self):
        for name in ('facade','door','roof'):
            changed=dict(self.tex)
            changed[name]=Image.new('RGBA',self.tex[name].size,(10,200,20,255))
            result=replay.render(self.mesh,changed)
            self.assertNotEqual(result.tobytes(),self.image.tobytes(),name)
            self.assertEqual(result.getchannel('A').tobytes(),self.image.getchannel('A').tobytes(),name)

    def test_hidden_surface_mutation_visible_in_reverse_only(self):
        changed=copy.deepcopy(self.mesh)
        changed['faces'][1]['material']='door'
        self.assertEqual(replay.render(changed,self.tex).tobytes(),self.image.tobytes())
        self.assertNotEqual(replay.render(changed,self.tex,True).tobytes(),replay.render(self.mesh,self.tex,True).tobytes())

    def test_output_hashes_native_half_obj(self):
        manifest=replay.load(P/'output/manifest.json')
        for name,digest in manifest['outputs'].items(): self.assertEqual(replay.sha(P/'output'/name),digest,name)
        for name,divisor in [('native-alpha.png',5),('half-alpha.png',10)]:
            with Image.open(P/'output'/name) as image:
                self.assertEqual(image.size,tuple(v//divisor for v in self.reg['sourceCanvas']))
                self.assertEqual(image.mode,'RGBA')
        obj=(P/'output/building.obj').read_text().splitlines()
        self.assertEqual(sum(line.startswith('v ') for line in obj),10)
        self.assertEqual(sum(line.startswith('f ') for line in obj),7)
        self.assertEqual(sum(line.startswith('vt ') for line in obj),30)

    def test_standalone_replay_without_repository_or_siblings(self):
        with tempfile.TemporaryDirectory(prefix='portable-',dir=P) as directory:
            root=Path(directory)
            for name in ('author.py','replay.py','mesh.json','materials.json'):
                shutil.copyfile(P/name,root/name)
            shutil.copytree(P/'inputs',root/'inputs')
            result=subprocess.run([sys.executable,'-I',str(root/'replay.py'),'--out',str(root/'output')],cwd=root,capture_output=True,text=True)
            self.assertEqual(result.returncode,0,result.stderr)
            expected=replay.load(P/'output/manifest.json')
            actual=replay.load(root/'output/manifest.json')
            self.assertEqual(actual,expected)
            for name in expected['outputs']:
                self.assertEqual((root/'output'/name).read_bytes(),(P/'output'/name).read_bytes(),name)

if __name__=='__main__': unittest.main(verbosity=2)
