"""Technical acceptance for one source comparison, not visual acceptance."""
import copy
import hashlib
import importlib.util
import json
import math
from pathlib import Path
import sys
import unittest
from PIL import Image, ImageChops

sys.dont_write_bytecode=True
HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('architecture_build',HERE/'build.py')
b=importlib.util.module_from_spec(spec)
spec.loader.exec_module(b)
OUT=HERE/'output'


def load(name):
    return json.loads((OUT/name).read_text())


class SourceComparisonTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.current=load('current-geometry.json')
        cls.proposal=load('proposed-geometry.json')
        cls.contract=load('scene-contract.json')
        cls.manifest=load('manifest.json')
        cls.records=json.loads((b.V9/'native-capture-v9/source-scene-records.json').read_text())
        cls.capture=next(c for c in cls.records['captures'] if c['arm']=='candidate' and c['zoom']==1)
        cls.assembly=json.loads((b.V9/'assembly.json').read_text())

    def test_all_five_current_meshes_exact_extraction(self):
        self.assertEqual(self.current,b.extract())
        self.assertEqual({x['solidID'] for x in self.current},{'solid-03-transit-kiosk','solid-01-residential-west','solid-02-residential-north','solid-04-civic-west','solid-05-civic-dais'})
        self.assertEqual(len(self.current),5)
        original=json.loads((b.OLD/'kiosk/output/mesh.json').read_text())
        self.assertEqual([f['vertices'] for f in self.current[0]['faces']],[[original['vertices'][i] for i in f['indices']] for f in original['faces']])

    def test_z_only_geometry_change_and_all_contacts(self):
        self.assertEqual(self.proposal,b.proposed(self.current))
        for old,new in zip(self.current,self.proposal):
            self.assertEqual(old['worldPosition'],new['worldPosition'])
            self.assertEqual(old['footprintWorld'],new['footprintWorld'])
            self.assertEqual(old['contactLocal'],new['contactLocal'])
            m=dict(b.mapping(old))
            values=list(m.values())
            self.assertEqual(values,sorted(set(values)))
            self.assertEqual(m[0],0)
            self.assertNotEqual(len(set(round(y/x,7) for x,y in m.items() if x)),1,'Not a uniform stretch')
            for f,g in zip(old['faces'],new['faces']):
                self.assertEqual(f['name'],g['name'])
                self.assertEqual(f['flatClass'],g['flatClass'])
                for p,q in zip(f['vertices'],g['vertices']):
                    self.assertEqual(p[:2],q[:2])
                    self.assertEqual(q[2],m[p[2]])
                    self.assertTrue(all(math.isfinite(v) for v in q))
                n=b.normal(g['vertices'])
                self.assertGreater(sum(v*v for v in n),0)

    def test_source_and_old_input_hashes_unchanged(self):
        self.assertEqual(self.manifest['implementationSHA256'],b.sha(HERE/'build.py'))
        for path,digest in self.manifest['inputs'].items():
            self.assertEqual(b.sha(b.ROOT/path),digest,path)
        for path,digest in self.manifest['outputs'].items():
            self.assertEqual(b.sha(OUT/path),digest,path)

    def test_reused_depth_complete_exact_and_permutation_stable(self):
        d=b.module('_test_arch_depth',b.ROOT/'docs/review/scene-qa-repair-20261116/native.py')
        result=d.depth_order(self.contract['depthItems'])
        self.assertEqual(result['order'],self.capture['depthOrder'])
        self.assertEqual(result['constraints'],self.capture['depthConstraints'])
        self.assertEqual(result,d.depth_order(list(reversed(self.contract['depthItems']))))
        self.assertEqual(len(result['order']),71)
        self.assertLess(result['order'].index('benchmark-building'),result['order'].index('sprite-camera-3'))

    def test_retained_authority_not_reauthored(self):
        for key in ('actors','supplementalActors','depthItems','depthOrder','depthConstraints','framing','centerWorld','groundPlanWitness'):
            self.assertEqual(self.contract[key],self.capture[key],key)
        for key,value in self.contract['cameraField'].items():
            self.assertEqual(value,self.capture[key])
        self.assertEqual(self.contract['fieldPolygonWorld'],b.field_polygon(self.capture))
        self.assertEqual(self.contract['zooms'],[1,1.25,1.4])
        self.assertFalse(self.contract['nativeEvidence'])
        self.assertFalse(self.contract['ownerAcceptance'])
        self.assertEqual(self.contract['attempt'],1)
        self.assertEqual(len(self.contract['omittedOffscreenActors']),9)
        for actor in self.contract['omittedOffscreenActors']:
            self.assertTrue(all(b.offscreen(actor,z) for z in b.ZOOMS))

    def test_player_camera_identical_registered_layers(self):
        sources={s['role']:s for s in self.assembly['sources']}
        for z in b.ZOOMS:
            for name,role in [('sprite-player','player'),('sprite-camera-3','camera')]:
                actor=next(a for a in self.capture['actors'] if a['name']==name)
                source=Image.open(b.ROOT/sources[role]['image']['path']).convert('RGBA')
                expected=b.registered_layer(source,b.actor_reg(actor,source),z)
                for arm in ('current','proposed'):
                    actual=Image.open(OUT/f'{arm}-{name}-z{round(z*100)}.png').convert('RGBA')
                    self.assertEqual(actual.tobytes(),expected.tobytes())
                self.assertEqual(b.sha(OUT/f'current-{name}-z{round(z*100)}.png'),b.sha(OUT/f'proposed-{name}-z{round(z*100)}.png'))

    def test_rendered_buildings_untextured_and_nonempty(self):
        for arm in ('current','proposed'):
            for building in self.current:
                im=Image.open(OUT/f'{arm}-{building["solidID"]}.png').convert('RGBA')
                colors=im.getcolors(im.width*im.height)
                self.assertLessEqual(len(colors),16,'No facade textures or noise')
                self.assertTrue(im.getchannel('A').getbbox())
                self.assertGreater(im.getchannel('A').histogram()[0],0)

    def test_geometry_registration_contacts_and_vertical_displacement(self):
        regs=load('registrations.json')
        for old,new in zip(self.current,self.proposal):
            for arm,building in [('current',old),('proposed',new)]:
                reg=regs[arm][building['nodeName']]
                for p in building['contactLocal']:
                    local=b.project(p)
                    sx=reg['rootPixelsTopLeft'][0]+b.SOURCE_PPU*local[0]
                    sy=reg['rootPixelsTopLeft'][1]-b.SOURCE_PPU*local[1]
                    recovered=[(sx-reg['rootPixelsTopLeft'][0])/b.SOURCE_PPU,(reg['rootPixelsTopLeft'][1]-sy)/b.SOURCE_PPU]
                    self.assertAlmostEqual(local[0],recovered[0])
                    self.assertAlmostEqual(local[1],recovered[1])
                self.assertEqual(reg['worldPosition'],building['worldPosition'])
                self.assertEqual([n/b.SOURCE_PPU for n in reg['canvasPixels']],reg['drawSizeWorld'])

    def test_dimensions_against_real_geometry(self):
        report=load('dimensions.json')
        self.assertEqual(report['playerReference']['rootToAlphaTopWorld'],49.5)
        for row,old,new in zip(report['buildings'],self.current,self.proposal):
            measures=row['dimensions']
            for metric,value in measures.items():
                self.assertAlmostEqual(value['delta'],value['proposed']-value['current'])
                self.assertAlmostEqual(value['currentPlayerRatio'],value['current']/49.5)
                self.assertAlmostEqual(value['proposedPlayerRatio'],value['proposed']/49.5)
            if 'facadeTop' in measures:
                self.assertEqual(measures['facadeTop']['current'],old['authoredHeight'])
                self.assertEqual(measures['facadeTop']['proposed'],new['authoredHeight'])
            if 'storeyPitch' in measures:
                for arm,building in [('current',old),('proposed',new)]:
                    faces={f['name']:f for f in building['faces']}
                    low=min(v[2] for v in faces['south-0-f0-glazing/south']['vertices'])
                    upper=min(v[2] for v in faces['south-0-f1-glazing/south']['vertices'])
                    high=max(v[2] for v in faces['south-0-f0-glazing/south']['vertices'])
                    self.assertEqual(upper-low,measures['storeyPitch'][arm])
                    self.assertEqual(high-low,measures['windowHeight'][arm])
            if 'kiosk' in row['solidID']:
                for arm,building in [('current',old),('proposed',new)]:
                    door=[v[2] for f in building['faces'] if f['flatClass']=='opening' and f['material']=='door' for v in f['vertices']]
                    self.assertAlmostEqual(max(door)-min(door),measures['doorClearance'][arm])

    def test_full_benchmark_pixels_and_three_comparison_sheets(self):
        original=Image.open(b.OLD/'kiosk/inputs/benchmark.png').convert('RGBA')
        retained=Image.open(OUT/'original-full-benchmark.png').convert('RGBA')
        self.assertEqual(original.size,retained.size)
        self.assertEqual(original.tobytes(),retained.tobytes())
        for z in b.ZOOMS:
            code=round(z*100)
            self.assertEqual(Image.open(OUT/f'comparison-z{code}.png').size,(2112,1340))
            for arm in ('current','proposed'):
                self.assertEqual(Image.open(OUT/f'{arm}-z{code}.png').size,(2112,1008))

    def test_no_ghost_pixels_exact_recomposition_from_source_layers(self):
        """Complete pixel comparison from separate layers, never native screenshot paintover."""
        sources={s['role']:s for s in self.assembly['sources']}
        ground=Image.open(b.ROOT/sources['ground-plan']['image']['path']).convert('RGBA')
        regs=load('registrations.json')
        known={x['nodeName'] for x in self.current}
        for zoom in b.ZOOMS:
            layers={}
            for actor in self.capture['actors']:
                name=actor['name']
                if name in known or actor in self.contract['omittedOffscreenActors']:
                    continue
                if name in ('sprite-player','sprite-camera-3'):
                    path=b.ROOT/sources['player' if name=='sprite-player' else 'camera']['image']['path']
                else:
                    path=b.ROOT/'AppTests/BenchmarkAssets'/('newsbox.png' if name.endswith('0') else 'tree.png')
                im=Image.open(path).convert('RGBA')
                layers[name]=b.registered_layer(im,b.actor_reg(actor,im),zoom)
            for s in self.assembly['supplements']:
                layers[s['nodeName']]=b.registered_layer(Image.open(b.V9/'native-inputs-v9'/s['file']).convert('RGBA'),s['registration'],zoom)
            base=b.ground_layer(ground,self.capture,zoom)
            for arm in ('current','proposed'):
                all_layers=dict(layers)
                for building in self.current:
                    im=Image.open(OUT/f'{arm}-{building["solidID"]}.png').convert('RGBA')
                    all_layers[building['nodeName']]=b.registered_layer(im,regs[arm][building['nodeName']],zoom)
                composed=base.copy()
                for name in self.capture['depthOrder']:
                    if name in all_layers:
                        composed=Image.alpha_composite(composed,all_layers[name])
                expected=Image.open(OUT/f'{arm}-z{round(zoom*100)}.png').convert('RGB').crop((0,30,2112,1008))
                self.assertEqual(composed.convert('RGB').tobytes(),expected.tobytes())

    def test_existing_output_fail_closed(self):
        with self.assertRaisesRegex(RuntimeError,'immutable'):
            b.build(OUT)


if __name__=='__main__':
    unittest.main(verbosity=2)
