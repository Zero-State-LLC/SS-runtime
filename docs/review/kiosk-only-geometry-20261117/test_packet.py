"""Frozen-input, geometry, authority, raster and mutation checks. No native claims."""
import copy
import json
from pathlib import Path
import unittest
from PIL import Image, ImageChops
import build as b

OUT=b.HERE/'output'


def load(name):
    return json.loads((OUT/name).read_text())


def im(name):
    return Image.open(OUT/name).convert('RGBA')


def verify_authority(contract, baseline):
    assert contract['sourceRecord']==baseline, 'Changed V9 authority'
    assert contract['kind']=='SOURCE_PROXY_NOT_NATIVE'
    assert contract['nativeEvidence'] is False and contract['acceptance'] is False
    assert contract['centerWorld']==[684,724]
    assert contract['canvasPixels']==[2112,978]
    assert contract['zooms']==[1,1.25,1.4]


class KioskOnly(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.old=load('current-geometry.json')
        cls.new=load('proposed-geometry.json')
        cls.contract=load('scene-contract.json')
        cls.live,cls.record,cls.records,cls.ground,cls.retained,cls.bindings,cls.omitted=b.inputs()

    def test_complete_hash_closure(self):
        manifest=load('manifest.json')
        for p,h in manifest['inputs'].items():
            self.assertEqual(b.a.sha(b.ROOT/p),h,p)
        for p,h in manifest['outputs'].items():
            self.assertEqual(b.a.sha(OUT/p),h,p)
        self.assertEqual(set(manifest['outputs']),{p.name for p in OUT.iterdir() if p.is_file()}-{'manifest.json'})

    def test_current_is_exact_source_extraction(self):
        self.assertEqual(self.old,self.live)

    def test_only_declared_z_changes(self):
        b.validate_geometry(self.old,self.new)
        self.assertEqual(self.new,b.proposed(self.live))
        self.assertEqual(self.old[1:],self.new[1:])
        prior=json.loads((b.ADAPTER.parent/'output/proposed-geometry.json').read_text())
        self.assertEqual(self.new[0],prior[0])
        for old,new in zip(self.old[1:],prior[1:]):
            self.assertNotEqual(old,new,'Earlier broad redesign must not silently match current neighbors')

    def test_all_contact_and_authority_envelopes_exact(self):
        for old,new in zip(self.old,self.new):
            for field in ('worldPosition','footprintWorld','contactLocal'):
                self.assertEqual(old.get(field),new.get(field))
            contacts=lambda x:[v for f in x['faces'] for v in f['vertices'] if v[2]==0]
            self.assertEqual(contacts(old),contacts(new))
        self.assertEqual(self.old[0]['footprintWorld'],dict(minWorld=[512,640],maxWorld=[640,768]))
        self.assertEqual(self.old[0]['contactLocal'],[[39,0,0],[128,0,0],[128,128,0],[0,128,0],[0,39,0]])

    def test_neighbor_mutation_rejected(self):
        for index in range(1,5):
            mutated=copy.deepcopy(self.new)
            mutated[index]['faces'][0]['vertices'][0][2]+=1
            with self.assertRaisesRegex(AssertionError,'Neighbor'):
                b.validate_geometry(self.old,mutated)

    def test_kiosk_xy_mutation_rejected(self):
        mutated=copy.deepcopy(self.new)
        mutated[0]['faces'][0]['vertices'][0][0]+=.01
        with self.assertRaisesRegex(AssertionError,'XY'):
            b.validate_geometry(self.old,mutated)

    def test_undeclared_z_mutation_rejected(self):
        mutated=copy.deepcopy(self.new)
        mutated[0]['faces'][0]['vertices'][0][2]+=.01
        with self.assertRaisesRegex(AssertionError,'Undeclared'):
            b.validate_geometry(self.old,mutated)

    def test_kiosk_topology_material_footprint_mutations_rejected(self):
        for mutation in ('topology','material','footprint','root','contact'):
            m=copy.deepcopy(self.new)
            if mutation=='topology':m[0]['faces'].pop()
            if mutation=='material':m[0]['faces'][0]['material']='invented'
            if mutation=='footprint':m[0]['footprintWorld']['minWorld'][0]+=1
            if mutation=='root':m[0]['worldPosition'][0]+=1
            if mutation=='contact':m[0]['contactLocal'][0][0]+=1
            with self.assertRaises(AssertionError,msg=mutation):b.validate_geometry(self.old,m)

    def test_full_v9_actor_field_depth_ground_framing_authority(self):
        verify_authority(self.contract,self.record)
        self.assertEqual(self.contract['bindings'],self.bindings)
        self.assertEqual(self.contract['omittedOffscreenActors'],self.omitted)
        self.assertEqual(len(self.record['depthOrder']),71)
        self.assertEqual(len(self.omitted),9)

    def test_actor_depth_ground_mutations_rejected(self):
        for key in ('actors','depthOrder','groundPlanWitness','cameraRange','framing','solids','controlsRetained'):
            c=copy.deepcopy(self.contract)
            c['sourceRecord'][key]=None
            with self.assertRaisesRegex(AssertionError,'authority'):verify_authority(c,self.record)

    def test_dimensions_from_semantic_faces(self):
        diff=load('dimension-diff.json')['dimensions']
        for arm,mesh in [('current',self.old[0]),('proposed',self.new[0])]:
            zs=lambda faces:[v[2] for f in faces for v in f['vertices']]
            door=zs([f for f in mesh['faces'] if f['material']=='door' and f['flatClass']=='opening'])
            roof=zs([f for f in mesh['faces'] if f['material']=='roof'])
            self.assertEqual(min(door),diff['doorThreshold'][arm])
            self.assertEqual(max(door),diff['doorHead'][arm])
            self.assertEqual(max(door)-min(door),diff['doorClearance'][arm])
            self.assertEqual(max(zs(mesh['faces'])),diff['top'][arm])
            self.assertIn(diff['roofDeck'][arm],roof)
        self.assertEqual(diff['top']['current'],132)
        self.assertEqual(diff['top']['proposed'],104)
        self.assertEqual(diff['doorThreshold']['proposed'],18)
        self.assertEqual(diff['parapet']['proposed'],4)
        self.assertAlmostEqual(diff['cornice']['current'],24.2170542635659)
        self.assertEqual(diff['cornice']['proposed'],10)

    def test_fixed_plan_spacing(self):
        d=load('dimension-diff.json')
        self.assertEqual(d['spacing'],b.spacing(self.old,self.record))
        self.assertEqual(d['spacing'],b.spacing(self.new,self.record))
        self.assertEqual(d['spacing']['cameraRootToEnvelope'],16)
        self.assertEqual(d['spacing']['playerRootToEnvelope'],96)
        self.assertEqual(d['spacing']['neighbors']['solid-02-residential-north']['envelopeDistance'],0)
        self.assertEqual(d['playerVisualReference'],49.5)

    def test_all_retained_layers_and_full_scene_reconstruction(self):
        for capture in self.contract['captures']:
            zoom=capture['zoom']
            code=round(100*zoom)
            base=b.a.ground_layer(self.ground,self.record,zoom)
            self.assertEqual(b.rgba(base),b.rgba(im(f'ground-z{code}.png')))
            self.assertEqual(b.rgba(base),capture['groundRGBA'])
            layers={n:b.a.registered_layer(image,reg,zoom) for n,(image,reg) in self.retained.items()}
            hashes={n:b.rgba(image) for n,image in layers.items()}
            self.assertEqual(hashes,capture['currentRetainedLayers'])
            self.assertEqual(hashes,capture['proposedRetainedLayers'])
            for name in layers:
                if name.startswith('environment-upright') or name in ('sprite-player','sprite-camera-3'):
                    self.assertEqual(hashes[name],b.rgba(im(f'retained-{name}-z{code}.png')))
            for arm in ('current','proposed'):
                layers['benchmark-building']=im(f'{arm}-kiosk-layer-z{code}.png')
                # Independent ordered compositing loop, not build.compose().
                actual=base.copy()
                for name in self.record['depthOrder']:
                    if name in layers:actual=Image.alpha_composite(actual,layers[name])
                self.assertEqual(actual.tobytes(),im(f'{arm}-z{code}.png').tobytes())

    def test_changed_pixels_confined_to_kiosk_silhouettes(self):
        for code in (100,125,140):
            current,proposal=im(f'current-z{code}.png'),im(f'proposed-z{code}.png')
            difference=ImageChops.difference(current.convert('RGB'),proposal.convert('RGB'))
            self.assertIsNotNone(difference.getbbox())
            mask=ImageChops.lighter(im(f'current-kiosk-layer-z{code}.png').getchannel('A'),im(f'proposed-kiosk-layer-z{code}.png').getchannel('A')).point(lambda x:255 if x else 0)
            outside=Image.composite(Image.new('RGB',difference.size),difference,mask)
            self.assertIsNone(outside.getbbox(),'Non-kiosk pixels changed')

    def test_native_and_benchmark_reference_pixels_exact(self):
        original=Image.open(b.a.OLD/'kiosk/inputs/benchmark.png').convert('RGBA')
        self.assertEqual(original.tobytes(),im('original-full-benchmark.png').tobytes())
        for code in (100,125,140):
            native=Image.open(b.a.V9/f'native-capture-v9/source-scene-candidate-ordinary-z{code}-native.png').convert('RGBA')
            self.assertEqual(native.tobytes(),im(f'v9-native-reference-z{code}.png').tobytes())
            self.assertEqual(im(f'comparison-z{code}.png').size,(2112,1340))

    def test_editable_indexed_mesh_and_hashes(self):
        import export_editable as e
        root=b.HERE/'editable'
        manifest=json.loads((root/'manifest.json').read_text())
        old=json.loads((root/'current-indexed-mesh.json').read_text())
        new=json.loads((root/'candidate-indexed-mesh.json').read_text())
        e.validate(old,new)
        self.assertEqual(b.a.sha(root/'current-indexed-mesh.json'),manifest['sourceSHA256'])
        self.assertEqual(b.a.sha(b.ROOT/manifest['sourcePath']),manifest['sourceSHA256'])
        self.assertEqual(b.a.sha(b.HERE/'export_editable.py'),manifest['exporterSHA256'])
        self.assertEqual(b.a.sha(b.HERE/'z-map.json'),manifest['zMapSHA256'])
        self.assertEqual(b.a.sha(OUT/'manifest.json'),manifest['comparisonManifestSHA256'])
        for path,digest in manifest['outputs'].items():self.assertEqual(b.a.sha(root/path),digest)
        self.assertEqual((root/'DIMENSIONS.md').read_text(),e.report())

    def test_editable_uv_and_height_mutations_rejected(self):
        import export_editable as e
        root=b.HERE/'editable'
        old=json.loads((root/'current-indexed-mesh.json').read_text())
        new=json.loads((root/'candidate-indexed-mesh.json').read_text())
        for kind in ('UV','height','XY','Z'):
            changed=copy.deepcopy(new)
            if kind=='UV':changed['faces'][0]['uv'][0][0]+=.1
            if kind=='height':changed['height']+=1
            if kind=='XY':changed['vertices'][0][0]+=1
            if kind=='Z':changed['vertices'][0][2]+=1
            with self.assertRaises(AssertionError,msg=kind):e.validate(old,changed)

    def test_reproduction_every_file_byte_exact(self):
        replay=b.HERE/'reproduction'
        self.assertEqual({p.name for p in OUT.iterdir()},{p.name for p in replay.iterdir()})
        for p in OUT.iterdir():self.assertEqual(p.read_bytes(),(replay/p.name).read_bytes(),p.name)

    def test_output_overwrite_fails_closed(self):
        before=b.a.sha(OUT/'manifest.json')
        with self.assertRaisesRegex(RuntimeError,'Immutable'):b.build(OUT)
        self.assertEqual(before,b.a.sha(OUT/'manifest.json'))


if __name__=='__main__':
    unittest.main(verbosity=2)
