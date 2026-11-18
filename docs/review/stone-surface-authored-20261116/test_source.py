"""Technical source guards, never visual acceptance."""
import ast
import copy
import json
import math
import shutil
import tempfile
import unittest
from collections import Counter
from pathlib import Path
from PIL import Image
import replay as r
HERE=Path(__file__).resolve().parent

class AuthoredStoneTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.mesh=r.load(HERE/'mesh.json')
        cls.model=r.load(HERE/'model.json')
        cls.paint=r.load(HERE/'surface-paint.json')
        cls.reg=r.load(HERE/'registration.json')

    def test_closed_surfaces_outward_normals_and_nonzero_volume(self):
        for part in self.mesh:
            edge=Counter()
            volume=0
            for face in part['faces']:
                pts=[part['vertices'][i] for i in face]
                r.normal(*pts[:3])
                for a,b in zip(face,face[1:]+face[:1]):edge[(a,b)]+=1
                for k in range(1,len(pts)-1):
                    a,b,c=pts[0],pts[k],pts[k+1]
                    volume+=(a[0]*(b[1]*c[2]-b[2]*c[1])+a[1]*(b[2]*c[0]-b[0]*c[2])+a[2]*(b[0]*c[1]-b[1]*c[0]))/6
            for (a,b),count in edge.items():
                self.assertEqual(count,1,part['name'])
                self.assertEqual(edge[(b,a)],1,part['name'])
            self.assertGreater(volume,0,part['name'])

    def test_foundation_registered_to_unchanged_original_solid(self):
        arena=r.ROOT/'Sources/SurveillanceCore/Resources/contracts/civic-seam-arena-004.json'
        solid=next(s for s in r.load(arena)['permanentSolids'] if s['id']=='solid-03-transit-kiosk')
        self.assertEqual(solid,{'id':'solid-03-transit-kiosk','center':{'x':576,'y':704},'halfSize':{'x':64,'y':64}})
        self.assertEqual(r.sha(arena),self.reg['arenaSHA256'])
        self.assertEqual(self.model['worldRoot'],[512,640,0])
        self.assertEqual(self.model['extent'],[128,128])
        foundation=next(p for p in self.mesh if p['name']=='registered-foundation')
        for mark in self.reg['landmarks']:
            self.assertEqual(mark['world'],[mark['local'][i]+self.model['worldRoot'][i] for i in range(3)])
            self.assertEqual(mark['source'],list(r.project(mark['local'],self.model)))
            if mark['id']=='A': self.assertNotIn(mark['local'],foundation['vertices'])
            else:self.assertIn(mark['local'],foundation['vertices'])
        self.assertIsNone(self.reg['measuredReferenceGeometry'])
        self.assertFalse(self.reg['ownerAccepted'])
        self.assertFalse(self.reg['productionAdmitted'])

    def test_projection_and_uprights_have_not_changed(self):
        origin=r.project([0,0,0],self.model)
        x=r.project([128,0,0],self.model)
        y=r.project([0,128,0],self.model)
        self.assertAlmostEqual((x[1]-origin[1])/(x[0]-origin[0]),-.5)
        self.assertAlmostEqual((y[1]-origin[1])/(y[0]-origin[0]),.5)
        self.assertEqual(r.project([0,0,10],self.model),(560,835))
        self.assertAlmostEqual(x[0]-origin[0],128*math.sqrt(.5)*5)

    def test_windows_are_recessed_not_painted_over_filled_shell(self):
        parts={p['name']:p for p in self.mesh}
        self.assertNotIn('wall-mass-complete-hidden-back-and-floor',parts)
        self.assertNotIn('south-window-mullion-0',parts)
        for prefix,axis in [('south',1),('west',0)]:
            for bay in ('a','b'):
                glass=parts[f'{prefix}-bay-{bay}-back-glass']['vertices']
                reveal=parts[f'{prefix}-bay-{bay}-left-reveal']['vertices']
                self.assertGreater(min(p[axis] for p in glass)-min(p[axis] for p in reveal),6)
        leaf=parts['door-leaf']['vertices']
        pier=parts['entry-left-pier']['vertices']
        self.assertGreater(min(x+y for x,y,z in leaf)-min(x+y for x,y,z in pier),13)

    def test_stairs_separate_and_within_collision_rectangle(self):
        stairs=[p for p in self.mesh if p['group']=='stairs']
        self.assertEqual(len(stairs),3)
        for part in stairs:
            for x,y,z in part['vertices']:
                self.assertTrue(0<=x<=128 and 0<=y<=128 and z>=0)
            self.assertEqual(min(p[2] for p in part['vertices']),0)

    def test_authored_surface_sources_and_common_lighting(self):
        tree=ast.parse((HERE/'replay.py').read_text())
        imports=[n.names[0].name for n in ast.walk(tree) if isinstance(n,ast.Import)]
        self.assertNotIn('random',imports)
        self.assertNotIn('author_mesh',imports)
        source=(HERE/'replay.py').read_text()
        self.assertNotIn('%256',source)
        self.assertNotIn('effect_noise',source)
        for part in self.mesh:self.assertIn(part['material'],self.paint['surfaces'])
        direction=self.model['light']['direction']
        self.assertEqual(direction,[-.72,-.28,.64])
        self.assertEqual(self.model['light']['ambient']+self.model['light']['diffuse'],1)
        self.assertGreater(len(self.paint['surfaces']),40)

    def test_alpha_native_half_and_original_unchanged(self):
        for name,size in [('preview-alpha.png',(1120,960)),('native-alpha.png',(224,192)),('half-alpha.png',(112,96)),('building-alpha.png',(1120,960)),('stairs-alpha.png',(1120,960)),('hidden-surfaces.png',(1120,960))]:
            with Image.open(HERE/name) as im:
                self.assertEqual(im.mode,'RGBA')
                self.assertEqual(im.size,size)
                alpha=im.getchannel('A')
                self.assertEqual(alpha.getextrema(),(0,255))
                box=alpha.getbbox()
                self.assertTrue(box[0]>0 and box[1]>0 and box[2]<im.width and box[3]<im.height)
                for rgba in im.get_flattened_data():
                    if rgba[3]==0:self.assertEqual(rgba[:3],(0,0,0))
        self.assertEqual(r.sha(r.REFERENCE),'49aa35447230187e3eabe948cdc8eba6d6d465b2605d624e2cf7443f6cb69ffb')

    def test_direct_edits_change_actual_render(self):
        m=copy.deepcopy(self.model)
        m.update(canvas=[224,192],sourceRoot=[112,177],sourcePixelsPerWorldUnit=1)
        textures=r.paint_surfaces(self.paint)
        baseline=r.render(m,self.mesh,textures)
        edited=copy.deepcopy(self.mesh)
        door=next(p for p in edited if p['name']=='door-leaf')
        for vertex in door['vertices']:vertex[2]+=8
        self.assertNotEqual(baseline.tobytes(),r.render(m,edited,textures).tobytes())
        paint=copy.deepcopy(self.paint)
        paint['surfaces']['south-window-a']['base']=[150,20,20]
        self.assertNotEqual(baseline.tobytes(),r.render(m,self.mesh,r.paint_surfaces(paint)).tobytes())

    def test_direct_source_replay_is_byte_identical(self):
        temp=Path(tempfile.mkdtemp(prefix='replay-test-',dir=HERE))
        self.addCleanup(shutil.rmtree,temp)
        r.build(temp,quick=True)
        for name in ('preview-alpha.png','native-alpha.png','half-alpha.png','comparison.png','comparison-grayscale.png','registration.json'):
            self.assertEqual(r.sha(HERE/name),r.sha(temp/name),name)
        for p in (HERE/'surfaces').iterdir():
            self.assertEqual(r.sha(p),r.sha(temp/'surfaces'/p.name),p.name)

if __name__=='__main__':unittest.main(verbosity=2)
