"""Isolated kiosk Z correction. Retain exact V9 neighbor images and geometry."""
import argparse
import copy
import hashlib
import importlib.util
import json
import math
from pathlib import Path
import sys
from PIL import Image, ImageDraw

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
ADAPTER = ROOT / 'docs/review/architectural-scale-20261117/source/build.py'
ADAPTER_SHA = '220750cc0576f3314852dcf306661c066ec0499ff0d48a0caa9d1bd325bda3f3'
assert hashlib.sha256(ADAPTER.read_bytes()).hexdigest() == ADAPTER_SHA
spec = importlib.util.spec_from_file_location('kiosk_retained_adapter', ADAPTER)
a = importlib.util.module_from_spec(spec)
spec.loader.exec_module(a)
a.INPUTS[str(ADAPTER.relative_to(ROOT))] = ADAPTER_SHA
KIOSK = 'solid-03-transit-kiosk'


def rgba(im):
    return hashlib.sha256(im.tobytes()).hexdigest()


def proposed(current):
    config = a.read(HERE / 'z-map.json')
    assert config['solidID'] == KIOSK
    mapping = dict(config['anchors'])
    result = copy.deepcopy(current)
    target = next(b for b in result if b['solidID'] == KIOSK)
    assert set(mapping) == {v[2] for f in target['faces'] for v in f['vertices']}
    assert list(mapping) == sorted(mapping)
    assert list(mapping.values()) == sorted(set(mapping.values()))
    assert mapping[0] == 0
    for face in target['faces']:
        for vertex in face['vertices']:
            vertex[2] = mapping[vertex[2]]
    target['authoredHeight'] = mapping[target['authoredHeight']]
    return result


def validate_geometry(current, candidate):
    assert len(current) == len(candidate) == 5
    mapping = dict(a.read(HERE / 'z-map.json')['anchors'])
    changed = []
    for old, new in zip(current, candidate):
        if old['solidID'] != KIOSK:
            assert old == new, 'Neighbor geometry changed'
            continue
        restored = copy.deepcopy(new)
        assert len(old['faces']) == len(new['faces'])
        for f, g in zip(old['faces'], restored['faces']):
            assert len(f['vertices']) == len(g['vertices'])
            for v, w in zip(f['vertices'], g['vertices']):
                assert v[:2] == w[:2], 'Kiosk XY changed'
                assert w[2] == mapping[v[2]], 'Undeclared kiosk Z'
                if v[2] != w[2]:
                    changed.append((v[2], w[2]))
                w[2] = v[2]
        assert restored['authoredHeight'] == mapping[old['authoredHeight']]
        restored['authoredHeight'] = old['authoredHeight']
        assert restored == old, 'Kiosk non-Z metadata changed'
    assert changed


def inputs():
    assembly = a.read(a.V9 / 'assembly.json')
    records = a.read(a.V9 / 'native-capture-v9/source-scene-records.json')
    c = next(c for c in records['captures'] if c['arm'] == 'candidate' and c['zoom'] == 1)
    depth = a.module('kiosk_retained_depth', ROOT / 'docs/review/scene-qa-repair-20261116/native.py')
    order = depth.depth_order(c['depthItems'])
    assert order['order'] == c['depthOrder']
    assert order['constraints'] == c['depthConstraints']
    sources = {s['role']: s for s in assembly['sources']}
    current = a.extract()
    neighbors = {b['nodeName']: sources['context-' + b['solidID'].split('-')[1]] for b in current if b['solidID'] != KIOSK}
    retained, bindings, omitted = {}, {}, []
    for actor in c['actors']:
        name = actor['name']
        if name == 'benchmark-building':
            continue
        source = neighbors.get(name)
        if name in ('sprite-player', 'sprite-camera-3'):
            source = sources['player' if name == 'sprite-player' else 'camera']
        if source:
            path = ROOT / source['image']['path']
            assert a.sha(path) == source['image']['sha256']
            im = a.image(path)
            # Use native recorded actor transforms, including their float precision.
            reg = a.actor_reg(actor, im)
            assert reg['worldPosition'] == source['registration']['worldPosition']
            assert all(abs(x-y) < 0.00001 for x,y in zip(reg['drawSizeWorld'], source['registration']['drawSizeWorld']))
        elif name in ('benchmark-prop-0', 'benchmark-prop-1'):
            path = ROOT / 'AppTests/BenchmarkAssets' / ('newsbox.png' if name.endswith('0') else 'tree.png')
            assert a.sha(path) == records['controlSHA256'][path.name]
            im = a.image(path)
            reg = a.actor_reg(actor, im)
        else:
            assert all(a.offscreen(actor,z) for z in a.ZOOMS), name
            omitted.append(actor)
            continue
        retained[name] = (im, reg)
        bindings[name] = dict(path=str(path.relative_to(ROOT)), sha256=a.sha(path), registration=reg)
    for source in assembly['supplements']:
        path = a.V9 / 'native-inputs-v9' / source['file']
        assert a.sha(path) == source['sha256']
        retained[source['nodeName']] = (a.image(path), source['registration'])
        bindings[source['nodeName']] = dict(path=str(path.relative_to(ROOT)), sha256=a.sha(path), registration=source['registration'])
    ground_source = sources['ground-plan']
    ground = a.image(ROOT / ground_source['image']['path'])
    assert ground_source['image']['sha256'] == c['groundPlanWitness']['sourceSHA256'] == a.sha(ROOT / ground_source['image']['path'])
    assert ground_source['registration']['drawSizeWorld'] == [2304,2304]
    return current, c, records, ground, retained, bindings, omitted


def measures(building):
    zs = sorted({v[2] for f in building['faces'] for v in f['vertices']})
    return dict(top=zs[15], roofDeck=zs[13], parapet=zs[15]-zs[13], cornice=zs[15]-zs[11], doorThreshold=zs[3], doorHead=zs[8], doorClearance=zs[8]-zs[3], windowSill=zs[6], windowHead=zs[8], windowHeight=zs[8]-zs[6], width=building['footprintWorld']['maxWorld'][0]-building['footprintWorld']['minWorld'][0], depth=building['footprintWorld']['maxWorld'][1]-building['footprintWorld']['minWorld'][1])


def spacing(current, c):
    box = current[0]['footprintWorld']
    lo, hi = box['minWorld'], box['maxWorld']
    def distance(p):
        return math.hypot(*[max(lo[i]-p[i],0,p[i]-hi[i]) for i in range(2)])
    actors = {x['name']: x['worldRoot'] for x in c['actors']}
    neighbors = {}
    for b in current[1:]:
        low, high = b['footprintWorld']['minWorld'], b['footprintWorld']['maxWorld']
        gaps = [max(lo[i]-high[i],low[i]-hi[i],0) for i in range(2)]
        neighbors[b['solidID']] = dict(axisGaps=gaps, envelopeDistance=math.hypot(*gaps), authoredHeight=b['authoredHeight'])
    return dict(cameraRoot=actors['sprite-camera-3'], playerRoot=actors['sprite-player'], cameraRootToEnvelope=distance(actors['sprite-camera-3']), playerRootToEnvelope=distance(actors['sprite-player']), neighbors=neighbors, qualification='Plan distances to authority envelope, not rendered contours or traversable clearance. Identical in both arms.')


def compose(base, layers, order):
    scene = base.copy()
    for name in order:
        if name in layers:
            scene = Image.alpha_composite(scene, layers[name])
    return scene


def build(out):
    if out.exists():
        raise RuntimeError('Immutable output exists. Choose a new empty path, preserve all failure evidence.')
    out.mkdir(parents=True)
    current, c, records, ground, retained, bindings, omitted = inputs()
    candidate = proposed(current)
    validate_geometry(current, candidate)
    a.dump(out / 'current-geometry.json', current)
    a.dump(out / 'proposed-geometry.json', candidate)
    old, new = measures(current[0]), measures(candidate[0])
    player = retained['sprite-player'][0]
    reference = (336-player.getchannel('A').getbbox()[1])/6
    diff = {k:dict(current=v, proposed=new[k], delta=new[k]-v, currentPlayerRatio=v/reference, proposedPlayerRatio=new[k]/reference) for k,v in old.items()}
    a.dump(out/'dimension-diff.json', dict(dimensions=diff, playerVisualReference=reference, spacing=spacing(current,c), zMap=a.read(HERE/'z-map.json'), neighborsUnchanged=True, units='Authored world units, not meters'))
    rasters = {}
    registrations = {}
    for arm, geometry in [('current',current),('proposed',candidate)]:
        im, reg = a.render(geometry[0])
        im.save(out/f'{arm}-kiosk.png')
        rasters[arm] = (im,reg)
        registrations[arm] = reg
    a.dump(out/'kiosk-registrations.json',registrations)
    benchmark = a.image(a.OLD/'kiosk/inputs/benchmark.png')
    benchmark.save(out/'original-full-benchmark.png')
    captures=[]
    for zoom in a.ZOOMS:
        code=round(zoom*100)
        base=a.ground_layer(ground,c,zoom)
        base.save(out/f'ground-z{code}.png')
        retained_layers={n:a.registered_layer(im,reg,zoom) for n,(im,reg) in retained.items()}
        hashes={n:rgba(im) for n,im in retained_layers.items()}
        for n,im in retained_layers.items():
            if n.startswith('environment-upright') or n in ('sprite-player','sprite-camera-3'):
                im.save(out/f'retained-{n}-z{code}.png')
        scenes={}
        for arm,(im,reg) in rasters.items():
            layers=dict(retained_layers)
            layers['benchmark-building']=a.registered_layer(im,reg,zoom)
            layers['benchmark-building'].save(out/f'{arm}-kiosk-layer-z{code}.png')
            scenes[arm]=compose(base,layers,c['depthOrder'])
            scenes[arm].save(out/f'{arm}-z{code}.png')
            a.labeled(scenes[arm],f'{arm.upper()} KIOSK ONLY | SOURCE PROXY NOT NATIVE | V9 NEIGHBORS UNCHANGED | z{zoom}').save(out/f'{arm}-z{code}-labeled.png')
        native_path=a.V9/f'native-capture-v9/source-scene-candidate-ordinary-z{code}-native.png'
        native=a.image(native_path)
        record=next(x for x in records['captures'] if x['arm']=='candidate' and x['zoom']==zoom)
        assert a.sha(native_path)==record['pngSHA256']['-native']
        native.save(out/f'v9-native-reference-z{code}.png')
        sheet=Image.new('RGB',(2112,1340),(31,34,35))
        for im,title,x,y in [(benchmark,'ORIGINAL FULL BENCHMARK / UNCROPPED',0,0),(native,f'UNCHANGED V9 NATIVE REFERENCE z{zoom}',1056,0),(scenes['current'],f'CURRENT KIOSK / SOURCE PROXY z{zoom}',0,670),(scenes['proposed'],f'KIOSK-ONLY Z CANDIDATE / SOURCE PROXY z{zoom}',1056,670)]:
            fit=im.copy()
            fit.thumbnail((1056,600),Image.Resampling.LANCZOS)
            sheet.paste(fit,(x+(1056-fit.width)//2,y+35))
            ImageDraw.Draw(sheet).text((x+10,y+10),title,fill='white')
        ImageDraw.Draw(sheet).text((12,1320),'Neighbors/actors/ground/depth unchanged. Proxy omits HUD/controls/shadow/kiosk vent. No acceptance or native integration.',fill='white')
        sheet.save(out/f'comparison-z{code}.png')
        captures.append(dict(zoom=zoom,currentRetainedLayers=hashes,proposedRetainedLayers=hashes,groundRGBA=rgba(base)))
        print('Rendered kiosk-only comparison',zoom,flush=True)
    # Complete original authority record makes silent non-kiosk changes detectable.
    a.dump(out/'scene-contract.json',dict(kind='SOURCE_PROXY_NOT_NATIVE',nativeEvidence=False,acceptance=False,sourceRecord=c,bindings=bindings,omittedOffscreenActors=omitted,captures=captures,zooms=list(a.ZOOMS),canvasPixels=list(a.SIZE),centerWorld=[684,724],limitations=['Only kiosk is untextured in comparison arms','Native HUD/controls/player shadow/kiosk raster vent omitted','Pillow source sampling and field raster are not SpriteKit','No horizontal spacing correction','No art acceptance or production admission']))
    for path in [HERE/'build.py',HERE/'DESIGN.md',HERE/'z-map.json']:
        a.INPUTS[str(path.relative_to(ROOT))]=a.sha(path)
    a.dump(out/'manifest.json',dict(schema='kiosk-only-comparison-001',inputs=a.INPUTS,outputs={p.name:a.sha(p) for p in sorted(out.iterdir()) if p.is_file()},nativeEvidence=False,acceptance=False))
    print('Manifest SHA256',a.sha(out/'manifest.json'),flush=True)


if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--out',type=Path,default=HERE/'output')
    build(parser.parse_args().out)
