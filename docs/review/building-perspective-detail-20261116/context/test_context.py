"""Independent footprint oracle and bounded standalone source regression tests."""
import copy
import hashlib
import json
import math
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
from PIL import Image, ImageChops
import replay

HERE=Path(__file__).resolve().parent
EXPECTED=['solid-01-residential-west','solid-02-residential-north','solid-04-civic-west','solid-05-civic-dais']
def load(name): return json.loads((HERE/name).read_text())
def sha(path): return hashlib.sha256(path.read_bytes()).hexdigest()

def alignment(registrations,geometry,records):
    capture=next(c for c in records['captures'] if c['arm']=='candidate' and c['zoom']==1)
    assert capture['solidCount']==len(capture['solids'])==24
    assert [r['solidID'] for r in registrations]==EXPECTED
    checks=[]
    for reg,building in zip(registrations,geometry['buildings']):
        authority=next(s for s in capture['solids'] if s['id']==reg['solidID'])
        node=next(n for n in capture['preprojectionInventory'] if n['name']==reg['nodeName'])
        assert reg['worldPosition']==building['worldPosition']==node['worldRoot']
        assert reg['footprintWorld']==building['footprintWorld']==authority
        assert all(reg['worldPosition'][axis]==(authority['minWorld'][axis]+authority['maxWorld'][axis])/2 for axis in (0,1))
        ratios=[reg['canvasPixels'][i]/reg['drawSizeWorld'][i] for i in (0,1)]
        assert ratios[0]==ratios[1]==geometry['pixelsPerWorldUnit']
        rx,ry=reg['rootPixelsTopLeft']
        scale=ratios[0]
        corners={(x,y) for x in (authority['minWorld'][0],authority['maxWorld'][0]) for y in (authority['minWorld'][1],authority['maxWorld'][1])}
        assert len(reg['geometryLandmarks'])==4
        assert {tuple(p['worldXYZ'][:2]) for p in reg['geometryLandmarks']}==corners
        maxerror=0
        for point in reg['geometryLandmarks']:
            assert point['localXYZ'] in [v for f in building['faces'] if f['name'].startswith('authoritative-contact-plinth/') for v in f['vertices']]
            assert point['localXYZ'][2]==point['worldXYZ'][2]==0
            u=(point['sourcePixelsTopLeft'][0]-rx)/scale
            v=(ry-point['sourcePixelsTopLeft'][1])/scale
            # Inverse projection derived algebraically here, without importing renderer projection.
            recovered=[(u+2*v)/math.sqrt(2)+reg['worldPosition'][0],(2*v-u)/math.sqrt(2)+reg['worldPosition'][1]]
            error=max(abs(recovered[i]-point['worldXYZ'][i]) for i in (0,1))
            maxerror=max(maxerror,error)
            assert error<1e-9, (reg['solidID'],point['name'],error)
        checks.append({'solidID':reg['solidID'],'originalWorldRoot':node['worldRoot'],'fourFootprintCornersChecked':4,'maxInverseResidualWorld':maxerror,'status':'PASS'})
    return checks

class ContextTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.geometry=load('geometry.json')
        cls.regs=load('registration.json')
        cls.records=load('inputs/v6-records.json')

    def test_exact_role_roots_authority_and_inverse_alignment(self):
        result=alignment(self.regs,self.geometry,self.records)
        self.assertEqual(len(result),4)

    def test_registration_mutations_rejected(self):
        for field in ('worldPosition','rootPixelsTopLeft','drawSizeWorld'):
            broken=copy.deepcopy(self.regs)
            broken[0][field][0]+=1
            with self.assertRaises(AssertionError): alignment(broken,self.geometry,self.records)
        broken=copy.deepcopy(self.regs)
        broken.pop()
        with self.assertRaises(AssertionError): alignment(broken,self.geometry,self.records)
        broken=copy.deepcopy(self.regs)
        broken[0]['geometryLandmarks'][0]['sourcePixelsTopLeft'][1]+=2
        with self.assertRaises(AssertionError): alignment(broken,self.geometry,self.records)

    def test_every_vertex_is_inside_original_footprint(self):
        for building in self.geometry['buildings']:
            bounds=building['footprintWorld']
            for face in building['faces']:
                self.assertEqual(len(face['vertices']),4)
                self.assertEqual(len(face['uv']),4)
                for v in face['vertices']:
                    self.assertGreaterEqual(v[2],0)
                    for i in (0,1):
                        world=v[i]+building['worldPosition'][i]
                        self.assertGreaterEqual(world,bounds['minWorld'][i])
                        self.assertLessEqual(world,bounds['maxWorld'][i])

    def test_all_geometric_landmarks_fit_registered_canvas(self):
        for reg,building in zip(self.regs,self.geometry['buildings']):
            for face in building['faces']:
                for x,y,z in face['vertices']:
                    # Independent basis multiplication, including upright z.
                    px=reg['rootPixelsTopLeft'][0]+(x*.7071067811865475-y*.7071067811865475)*reg['pixelsPerWorldUnit']
                    py=reg['rootPixelsTopLeft'][1]-(x*.3535533905932738+y*.3535533905932738+z)*reg['pixelsPerWorldUnit']
                    self.assertGreaterEqual(px,23.99)
                    self.assertGreaterEqual(py,23.99)
                    self.assertLessEqual(px,reg['canvasPixels'][0]-23.99)
                    self.assertLessEqual(py,reg['canvasPixels'][1]-23.99)

    def test_alpha_and_native_half_sizes(self):
        for reg in self.regs:
            self.assertEqual(sha(HERE/reg['source']),reg['sha256'])
            with Image.open(HERE/reg['source']) as im:
                self.assertEqual(im.mode,'RGBA')
                self.assertEqual(list(im.size),reg['canvasPixels'])
                self.assertEqual(im.getpixel((0,0))[3],0)
                alpha=im.getchannel('A')
                self.assertIsNotNone(alpha.getbbox())
                self.assertGreater(alpha.histogram()[255],im.width*im.height*.2)
            with Image.open(HERE/'output'/f"{reg['solidID']}-native.png") as im:
                self.assertEqual(im.size,tuple(round(v) for v in reg['drawSizeWorld']))
                native=im.size
            with Image.open(HERE/'output'/f"{reg['solidID']}-half.png") as im:
                self.assertEqual(im.size,tuple(round(v/2) for v in native))

    def test_provenance_and_manifest(self):
        for row in load('provenance.json')['inputs']:
            self.assertEqual(sha(HERE/row['localPath']),row['sha256'])
        manifest=load('manifest.json')
        for name,digest in manifest['implementationSHA256'].items():
            self.assertEqual(sha(HERE/name),digest)
        for relative,digest in manifest['files'].items():
            path=Path(relative)
            self.assertFalse(path.is_absolute())
            self.assertNotIn('..',path.parts)
            self.assertEqual(sha(HERE/path),digest)

    def test_uv_geometry_and_material_editability(self):
        spec=copy.deepcopy(self.geometry)
        spec['pixelsPerWorldUnit']=.5
        spec['paddingPixels']=3
        building=copy.deepcopy(spec['buildings'][-1])
        textures=replay.materials(HERE)
        base=replay.render(building,spec,textures)[0]
        altered=copy.deepcopy(building)
        for face in altered['faces']:
            if face['name'].startswith('raised-paving/roof/'):
                face['uv']=[[.25,0],[.75,0],[.75,1],[.25,1]]
        self.assertNotEqual(base.tobytes(),replay.render(altered,spec,textures)[0].tobytes())
        altered=copy.deepcopy(building)
        for face in altered['faces']:
            if face['name'].startswith('balustrade-top'):
                for v in face['vertices']: v[2]+=6
        changed=replay.render(altered,spec,textures)[0]
        self.assertNotEqual((base.size,base.tobytes()),(changed.size,changed.tobytes()))
        textures['roof']=textures['roof'].convert('L').convert('RGBA')
        self.assertNotEqual(base.tobytes(),replay.render(building,spec,textures)[0].tobytes())

    def test_nonaffine_uv_or_geometry_fails_closed(self):
        spec=copy.deepcopy(self.geometry)
        spec['pixelsPerWorldUnit']=.25
        textures=replay.materials(HERE)
        for key in ('vertices','uv'):
            building=copy.deepcopy(spec['buildings'][-1])
            building['faces'][0][key][2][0]+=.1
            with self.assertRaisesRegex(ValueError,'Non-affine'):
                replay.render(building,spec,textures)

    def test_roof_uv_density_is_world_consistent(self):
        self.assertEqual(self.geometry['roofTileWorldUnits'],128)
        count=0
        for building in self.geometry['buildings']:
            for face in building['faces']:
                if face['material'] != 'roof' or face['normal'] != [0,0,1]: continue
                count+=1
                for i in (1,3):
                    world=math.dist(face['vertices'][0],face['vertices'][i])
                    uv=math.dist(face['uv'][0],face['uv'][i])
                    self.assertAlmostEqual(world/uv,128,places=7)
                for uv in face['uv']:
                    self.assertTrue(all(-1e-9 <= v <= 1+1e-9 for v in uv))
        self.assertGreater(count,8)

    def test_roof_density_rejects_original_rectangular_stretch(self):
        original=json.loads((HERE/'attempt-01/geometry.json').read_text())
        face=next(f for f in original['buildings'][0]['faces'] if f['name']=='masonry-shell/roof')
        density=[math.dist(face['vertices'][0],face['vertices'][i])/math.dist(face['uv'][0],face['uv'][i]) for i in (1,3)]
        self.assertEqual(density,[122,506])
        self.assertNotAlmostEqual(*density)
        corrected=next(f for f in self.geometry['buildings'][0]['faces'] if f['name'].startswith('masonry-shell/roof/'))
        broken=copy.deepcopy(corrected)
        broken['uv']=[[0,0],[1,0],[1,1],[0,1]]
        actual=[math.dist(broken['vertices'][0],broken['vertices'][i])/math.dist(broken['uv'][0],broken['uv'][i]) for i in (1,3)]
        self.assertTrue(any(abs(d-128)>1e-7 for d in actual), 'Whole-face UV mutation must violate density')

    def test_standalone_replay_is_byte_identical(self):
        scratch=Path(os.environ.get('JCODE_SCRATCH_DIR',str(HERE/'scratch')))
        scratch.mkdir(parents=True,exist_ok=True)
        with tempfile.TemporaryDirectory(prefix='context-replay-',dir=scratch) as directory:
            target=Path(directory)
            shutil.copytree(HERE/'inputs',target/'inputs')
            for name in ('geometry.json','materials.json','provenance.json','replay.py','author.py','test_context.py','repair_roof_density.py'):
                shutil.copyfile(HERE/name,target/name)
            proc=subprocess.run([sys.executable,str(target/'replay.py')],cwd=target,env={**os.environ,'PYTHONPATH':''},capture_output=True,text=True,timeout=180)
            self.assertEqual(proc.returncode,0,proc.stdout+proc.stderr)
            self.assertEqual((target/'registration.json').read_bytes(),(HERE/'registration.json').read_bytes())
            self.assertEqual((target/'manifest.json').read_bytes(),(HERE/'manifest.json').read_bytes())
            for path in (HERE/'output').glob('*.png'):
                self.assertEqual(sha(path),sha(target/'output'/path.name),path.name)

if __name__=='__main__':
    suite=unittest.defaultTestLoader.loadTestsFromTestCase(ContextTests)
    result=unittest.TextTestRunner(verbosity=2).run(suite)
    if result.wasSuccessful():
        report={'status':'PASS','registrationSHA256':sha(HERE/'registration.json'),'geometrySHA256':sha(HERE/'geometry.json'),'v6RecordsSHA256':sha(HERE/'inputs/v6-records.json'),'checks':alignment(load('registration.json'),load('geometry.json'),load('inputs/v6-records.json')),'testCount':result.testsRun,'standaloneReplay':'PASS_BYTE_IDENTICAL','nativeCapture':False}
        (HERE/'alignment-verification.json').write_text(json.dumps(report,indent=2)+'\n')
    sys.exit(not result.wasSuccessful())
