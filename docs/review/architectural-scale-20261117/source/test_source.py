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
            with Image.open(OUT/f'comparison-z{code}.png') as sheet:
                self.assertEqual(sheet.size,(2112,1340))
            for arm in ('current','proposed'):
                with Image.open(OUT/f'{arm}-z{code}.png') as frame:
                    self.assertEqual(frame.size,(2112,978))
                    self.assertEqual(frame.width*326,frame.height*704)
                with Image.open(OUT/f'{arm}-z{code}-labeled.png') as labeled:
                    self.assertEqual(labeled.size,(2112,1008))

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
                expected=Image.open(OUT/f'{arm}-z{round(zoom*100)}.png').convert('RGB')
                self.assertEqual(composed.convert('RGB').tobytes(),expected.tobytes())

    def test_ground_square_source_uv_known_world_points(self):
        # Independent expected numbers from square source registration: u=2*x, v=4608-2*y.
        samples=[([0,0],[0,4608]),([2304,1536],[4608,1536]),([512,640],[1024,3328]),([736,654],[1472,3300]),([684,724],[1368,3160])]
        for world,expected in samples:
            actual=b.ground_source_uv(world,[4608,4608],2304)
            for x,y in zip(actual,expected):
                self.assertAlmostEqual(x,y,places=9)
        self.assertEqual(self.contract['groundSourceRegistration']['drawSizeWorld'],[2304,2304])
        self.assertEqual(self.contract['groundTextureRect'],[0,0,1,2/3])
        self.assertFalse(self.contract['hudAndControlsRendered'])
        self.assertEqual(self.contract['retainedControlAuthority'],self.capture['controlsRetained'])

    def test_technical_corrections_preserve_geometry_and_reference_layers(self):
        # Ground correction and normal-convention correction never reauthor geometry.
        for archive in ('attempt-01-ground-uv','attempt-02-face-normals'):
            first=HERE/archive/'output'
            for path in ('current-geometry.json','proposed-geometry.json','dimensions.json','registrations.json'):
                self.assertEqual(b.sha(first/path),b.sha(OUT/path),path)
            for arm in ('current','proposed'):
                # Kiosk uses cross-product convention throughout. Context raster changes
                # only because its explicit normals, not clockwise winding, are authority.
                name=f'{arm}-solid-03-transit-kiosk.png'
                self.assertEqual(b.sha(first/name),b.sha(OUT/name),name)
                for z in b.ZOOMS:
                    for actor in ('sprite-player','sprite-camera-3'):
                        name=f'{arm}-{actor}-z{round(z*100)}.png'
                        self.assertEqual(b.sha(first/name),b.sha(OUT/name),name)
            frozen=json.loads((first/'manifest.json').read_text())
            self.assertEqual(b.sha(HERE/archive/'build.py'),frozen['implementationSHA256'])
            for path,digest in frozen['outputs'].items():
                self.assertEqual(b.sha(first/path),digest,path)
        for z in b.ZOOMS:
            name=f'nonbuilding-ground-proxy-z{round(z*100)}.png'
            self.assertEqual(b.sha(HERE/'attempt-02-face-normals/output'/name),b.sha(OUT/name))

    def test_explicit_context_normals_and_culling_for_every_face(self):
        for buildings in (self.current,self.proposal):
            for building in buildings:
                for face in building['faces']:
                    if 'normal' in face:
                        self.assertEqual(b.face_normal(face),face['normal'])
                        x,y,z=face['normal']
                        self.assertEqual(b.visible_face(face),-x-y+math.sqrt(2)*z>0)
                        # The retained context intentionally uses the opposite winding.
                        self.assertLess(sum(a*c for a,c in zip(face['normal'],b.normal(face['vertices']))),0)
                    else:
                        self.assertEqual(b.face_normal(face),b.normal(face['vertices']))
                        self.assertIn('kiosk',building['solidID'])

    def test_independent_roof_interior_pixels_cover_all_five(self):
        regs=load('registrations.json')
        samples={'solid-03-transit-kiosk':([64,64],125,100),
                 'solid-01-residential-west':([0,0],112,150),
                 'solid-02-residential-north':([0,0],112,150),
                 'solid-04-civic-west':([40,0],142,120),
                 'solid-05-civic-dais':([0,5],13,9)}
        for arm,index in [('current',1),('proposed',2)]:
            for building in self.current:
                role=building['solidID']
                sample=samples[role]
                xyz=sample[0]+[sample[index]]
                # Independent D108 calculation, sampling roof away from edge/lantern.
                u=(xyz[0]-xyz[1])/math.sqrt(2)
                v=(xyz[0]+xyz[1])/(2*math.sqrt(2))+xyz[2]
                root=regs[arm][building['nodeName']]['rootPixelsTopLeft']
                x,y=math.floor(root[0]+3*u),math.floor(root[1]-3*v)
                im=Image.open(OUT/f'{arm}-{role}.png').convert('RGBA')
                self.assertEqual(im.getpixel((x,y)),(161,164,163,255),(arm,role,(x,y)))

    def test_dais_probe_accounts_for_rail_occlusion_at_pixel_center(self):
        # Independent ray/plane intersection: z=35 is retained south rail top.
        # Former center probe pixel(284,207) has u=1/6, v=53/6.
        # x-y=sqrt(2)*u, x+y=2*sqrt(2)*(v-35).
        root=load('registrations.json')['proposed']['environment-upright-env_solid_05_civic_dais']['rootPixelsTopLeft']
        self.assertEqual(root,[284,234])
        def rail_intersection(pixel):
            u=(pixel[0]+.5-root[0])/3
            v=(root[1]-pixel[1]-.5)/3
            total=2*math.sqrt(2)*(v-35)
            difference=math.sqrt(2)*u
            return [(total+difference)/2,(total-difference)/2]
        x,y=rail_intersection((284,207))
        self.assertTrue(-71 <= x <= 71 and -39 <= y <= -37)
        x,y=rail_intersection((273,201))
        self.assertFalse(-71 <= x <= 71 and -39 <= y <= -37)
        im=Image.open(OUT/'proposed-solid-05-civic-dais.png').convert('RGBA')
        self.assertEqual(im.getpixel((284,207)),(213,211,201,255),'Former probe must see actual top rail')
        self.assertEqual(im.getpixel((273,201)),(161,164,163,255),'Clear platform probe must see roof plane')

    def test_roof_plan_and_cornice_mass_report_independent_formulas(self):
        report=json.loads((HERE/'massing-measurements.json').read_text())
        for name,digest in report['sourceGeometrySHA256'].items():
            self.assertEqual(b.sha(OUT/name),digest)
        for row,building in zip(report['buildings'],self.current):
            lo,hi=building['footprintWorld']['minWorld'],building['footprintWorld']['maxWorld']
            w,d=hi[0]-lo[0],hi[1]-lo[1]
            for arm in ('current','proposed'):
                value=row[arm]
                self.assertEqual(value['meshWidth'],w)
                self.assertEqual(value['meshDepth'],d)
                if 'kiosk' in row['solidID']:
                    self.assertAlmostEqual(value['roofPlanArea']+value['copingPlanArea'],128*128-39*39/2)
                    self.assertAlmostEqual(value['parapetPrismEquivalentVolume'],value['copingPlanArea']*(7 if arm=='current' else 4))
                elif 'dais' in row['solidID']:
                    self.assertEqual(value['platformPlanArea'],(w-16)*(d-16))
                else:
                    self.assertEqual(value['roofPlanArea'],(w-6)*(d-6))
                    # Four2-wide strips: eaves height5, parapet6/4 inset1, coping2.
                    expected=(52*(w+d)-96) if arm=='current' else (44*(w+d)-64)
                    self.assertEqual(value['cornicePrismVolumeSum'],expected)

    def test_existing_output_fail_closed(self):
        with self.assertRaisesRegex(RuntimeError,'immutable'):
            b.build(OUT)


if __name__=='__main__':
    unittest.main(verbosity=2)
