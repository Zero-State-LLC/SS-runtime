"""Independent V9 source admission adapter. Consumes coordinator recommendation only.
ADAPT V8 scene/plan_binding.py:35-66 for strict dependency paths, not source authority.
"""
import hashlib
import importlib.util
import json
import math
from pathlib import Path
import re
from PIL import Image

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
SOURCE_ROOT = HERE.parent / 'source'
SOURCE = SOURCE_ROOT / 'attempt-02'
FINAL_MANIFEST_SHA256 = '5b0943d029eadaf00d4e2d039dbeeda3e3353241c7881f28dd370c3295ab1891'
V8 = HERE.parent.parent / 'footprint-ground-repair-20261116'
_VERIFIED = set()


def need(condition, message):
    if not condition:
        raise ValueError(message)


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def load(path):
    return json.loads(Path(path).read_text())


def module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    result = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(result)
    return result


def dependency(dep, root):
    need(isinstance(dep, dict) and set(dep) == {'path', 'sha256'}, 'Exact dependency fields required')
    path, digest = dep['path'], dep['sha256']
    need(isinstance(path, str) and path and not path.startswith('/') and '\\' not in path and all(p not in ('', '.', '..') for p in path.split('/')), 'Unsafe dependency path')
    need(isinstance(digest, str) and re.fullmatch('[0-9a-f]{64}', digest) is not None, 'Invalid dependency digest')
    root = root.resolve()
    result = root / path
    need(result.resolve() == result and result.is_file() and sha(result) == digest, 'Missing/symlinked/stale dependency: ' + path)
    return result


def finite(values, count):
    return isinstance(values, list) and len(values) == count and all(type(v) in (int, float) and math.isfinite(v) for v in values)


def same(actual, expected, label):
    need(finite(actual, len(expected)) and all(abs(x-y) <= 1e-8 for x, y in zip(actual, expected)), 'Geometry/registration mismatch: ' + label)


def validate_geometry(geometry, sprites, ids, props):
    """Re-derive source projection, exact extrusion, bounds and V8 curb cells.
    Does not infer geometry from rendered alpha, and does not trust source tests.
    """
    need(geometry.get('schema') == 'blocked-base-curb-geometry-009' and geometry.get('presentationOnly') is True, 'Unknown/nonpresentation geometry')
    need(type(geometry.get('attempt')) is int and geometry['attempt'] in (1, 2), 'Bounded attempt budget exceeded')
    need(geometry.get('baseEnvelopeWorld') == [512, 640, 640, 768] and geometry.get('baseTriangleWorld') == [[512,640],[551,640],[512,679]], 'Authoritative blocked corner changed')
    need(geometry.get('curbRegionWorld') == [452,572,984,796], 'Curb region escaped approved retained boundary')
    need(geometry.get('pixelsPerWorldUnit') == 4 and geometry.get('paddingPixels') == 4, 'Source projection scale/padding drift')
    need(geometry.get('props') == props, 'V8 prop plan drift')
    shapes = geometry.get('sprites', [])
    need(len(shapes) == len(sprites) and 2 <= len(shapes) <= 128, 'Explicit bounded sprite census')
    names = [s.get('id') for s in sprites]
    need(len(set(names)) == len(names) and names == [s.get('id') for s in shapes], 'Source/geometry identity census')
    need(sum(s.get('kind') == 'blocked-base' for s in shapes) == 1 and shapes[0].get('kind') == 'blocked-base', 'Exactly one base plus curbs')
    need(ids.mode == 'L' and ids.size == (4608,4608), 'Frozen semantic-ID raster required')
    covered = set()
    normalized = []
    for shape, sprite in zip(shapes, sprites):
        name, root = shape['id'], shape['worldPosition']
        need(isinstance(name, str) and re.fullmatch('v9-[a-z0-9-]+', name), 'Unsafe supplemental identity')
        need(finite(root, 2) and sprite['id'] == name and sprite['kind'] == shape['kind'], 'Supplement identity/root drift')
        contact = shape['contactLocal']
        need(isinstance(contact, list) and len(contact) in (3,4) and all(finite(p,3) and p[2] == 0 for p in contact), 'Actual Z0 contact polygon required')
        polygon = [[p[0]+root[0], p[1]+root[1],0] for p in contact]
        same(root, [sum(p[i] for p in polygon)/len(polygon) for i in (0,1)], 'contact-centroid root')
        h = shape['heightWorld']
        need(type(h) in (int,float) and h == (18 if shape['kind'] == 'blocked-base' else 3), 'Explicit approved vertical relief required')
        if shape['kind'] == 'blocked-base':
            need(polygon == [[512,640,0],[551,640,0],[512,679,0]], 'Base must cover exact omitted blocked triangle, not a ground patch')
        else:
            need(shape['kind'] == 'curb-relief' and len(polygon) == 4, 'Only bounded curb extrusions allowed')
            x0,y0 = polygon[0][:2]
            x1,y1 = polygon[2][:2]
            need(polygon == [[x0,y0,0],[x1,y0,0],[x1,y1,0],[x0,y1,0]] and 452 <= x0 < x1 <= 984 and 572 <= y0 < y1 <= 796, 'Curb must stay in approved material strip')
            need(all(v*2 == int(v*2) for v in (x0,y0,x1,y1)), 'Curb cells must align with existing semantic pixels')
            for y in range(int(y0*2),int(y1*2)):
                for x in range(int(x0*2),int(x1*2)):
                    need(ids.getpixel((x,4607-y)) == 2 and (x,y) not in covered, 'Curb overpaint/topology drift or duplicated cell')
                    covered.add((x,y))
            for prop in props:
                radius = max(prop['contactRadiusWorld'],prop['shadowRadiusWorld'])
                px,py = prop['worldRoot']
                dx,dy = max(x0-px,0,px-x1),max(y0-py,0,py-y1)
                need(math.hypot(dx,dy) > radius, 'Curb covers required prop contact/shadow region')
        faces = shape['faces']
        need(len(faces) == len(contact)+1, 'Closed upper prism cap/vertical face census')
        expected = [[[p[0],p[1],h] for p in contact]]
        for i,p in enumerate(contact):
            q=contact[(i+1)%len(contact)]
            expected.append([p,q,[q[0],q[1],h],[p[0],p[1],h]])
        need([f['vertices'] for f in faces] == expected, 'Supplement mesh differs from declared bounded prism')
        need(faces[0]['material'] == 'cap' and all(f['material'] == ('masonry' if shape['kind'] == 'blocked-base' else 'curb') for f in faces[1:]), 'Unbounded source material assignment')
        vertices = sorted(set(tuple(v) for f in faces for v in f['vertices']))
        world = [[v[0]+root[0],v[1]+root[1],v[2]] for v in vertices]
        bounds = dict(min=[min(v[i] for v in world) for i in range(3)],max=[max(v[i] for v in world) for i in range(3)])
        need(sprite['contactWorldXYZ'] == polygon and sprite['heightWorld'] == h and sprite['worldBoundsXYZ'] == bounds, 'Forged contacts/heights/bounds')
        need(sprite['geometryFile'] == 'geometry.json' and sprite['geometryID'] == name and sprite['pixelsPerWorldUnit'] == 4, 'Wrong geometry provenance')
        reg = sprite['registration']
        need(set(reg) == {'canvasPixels','rootPixelsTopLeft','worldPosition','drawSizeWorld'}, 'Exact registration fields')
        need(all(finite(reg[k],2) for k in reg) and reg['worldPosition'] == root, 'Invalid source registration')
        need(all(type(v) is int and 0 < v <= 2048 for v in reg['canvasPixels']), 'Invalid source canvas')
        same(reg['drawSizeWorld'], [v/4 for v in reg['canvasPixels']], 'source draw size')
        need(all(0 <= v <= c for v,c in zip(reg['rootPixelsTopLeft'],reg['canvasPixels'])), 'Anchor outside sprite')
        landmarks = sprite['geometryLandmarks']
        need([p['worldXYZ'] for p in landmarks] == world, 'All actual XYZ source vertices required')
        for local, landmark in zip(vertices,landmarks):
            u=(local[0]-local[1])/math.sqrt(2)
            v=(local[0]+local[1])/(2*math.sqrt(2))+local[2]
            same(landmark['sourcePixelsTopLeft'], [reg['rootPixelsTopLeft'][0]+4*u,reg['rootPixelsTopLeft'][1]-4*v], 'D108 XYZ source point')
        normalized.append(dict(role=name,nodeName='supplement-'+name,file=name+'.png',sha256=sprite['image']['sha256'],registration=reg,verticesWorldXYZ=world,verticesPixelsTopLeft=[v['sourcePixelsTopLeft'] for v in landmarks],footprintWorld=bounds['min'][:2]+bounds['max'][:2]))
    required = {(x,y) for y in range(1144,1592) for x in range(904,1968) if ids.getpixel((x,4607-y)) == 2}
    need(covered == required, 'Supplement curb coverage omits/invents existing semantic strip')
    return normalized


def validate(binding, root=ROOT):
    need(isinstance(binding, dict) and set(binding) == {'schema','manifest','dependencies','recommendation'}, 'Exact coordinator supplement envelope required')
    need(binding['schema'] == 'blocked-base-curb-recommendations-009', 'Unknown recommendation schema')
    root = root.resolve()
    directory = root / SOURCE.relative_to(ROOT)
    source_root = root / SOURCE_ROOT.relative_to(ROOT)
    path = dependency(binding['manifest'], root)
    need(path == directory/'manifest.json', 'Exact final manifest path required')
    need(binding['manifest']['sha256'] == FINAL_MANIFEST_SHA256, 'Pinned final attempt02 manifest required')
    rec = binding['recommendation']
    need(isinstance(rec,dict) and set(rec) == {'reviewerRole','decision','scope','manifestSHA256','evidence'}, 'Exact separate coordinator recommendation required')
    need(rec['reviewerRole'] == 'coordinator' and rec['decision'] == 'recommended' and rec['scope'] == 'isolated-ordinary-scene', 'Pending/rejected/source-worker recommendation forbidden')
    need(rec['manifestSHA256'] == binding['manifest']['sha256'], 'Stale final coordinator recommendation')
    evidence = dependency(rec['evidence'],root)
    need(source_root not in evidence.parents and evidence != source_root, 'Any source descendant cannot supply its own recommendation evidence')
    manifest = load(path)
    need(manifest.get('schema') == 'blocked-base-curb-source-009' and type(manifest.get('attempt')) is int and manifest['attempt'] == manifest.get('maximumAttempts') == 2, 'Only final bounded attempt02 source allowed')
    need(manifest.get('status') == 'FINAL_CORRECTION_PENDING_COORDINATOR' and manifest.get('sourceRecommendation') is None and manifest.get('nativeEvidence') is False, 'Final source cannot self-recommend or claim native evidence')
    files = manifest.get('files',{})
    required = {'geometry.json','materials.json','replay.py','author.py','test_source.py','attempt-01-frozen-sha256.json','output/registration.json','ADAPT.md'}
    need(isinstance(files,dict) and required <= set(files), 'Missing editable source/validator dependencies')
    dependencies = []
    for name,digest in sorted(files.items()):
        need(isinstance(name,str) and name and not name.startswith('/') and '\\' not in name and all(p not in ('','.','..') for p in name.split('/')), 'Source manifest path escape')
        dep = dict(path=str((directory/name).relative_to(root)),sha256=digest)
        dependency(dep,root)
        dependencies.append(dep)
    need(binding['dependencies'] == dependencies, 'Exact complete source dependency list required')
    baseline = load(source_root/'baseline-sha256.json')
    final_baseline = manifest.get('baselineFiles')
    need(isinstance(final_baseline,dict) and baseline and all(final_baseline.get(name) == digest for name,digest in baseline.items()), 'Missing immutable V8 dependencies')
    for name,digest in final_baseline.items():
        dependency(dict(path=name,sha256=digest),root)
    first = load(directory/'attempt-01-frozen-sha256.json')
    need(isinstance(first,dict) and first and manifest.get('firstAttemptFiles') == first, 'Missing or changed first-attempt freeze')
    for name,digest in first.items():
        dependency(dict(path=name,sha256=digest),root)
    need(sha(directory/'geometry.json') == sha(source_root/'geometry.json'), 'Final material correction changed original geometry bytes')
    frozen = root / V8.relative_to(ROOT)
    # Full V8 adapter separately revalidates its authoritative/source contracts.
    need(sha(frozen/'scene/native-capture-v8/source-scene-records.json') == 'f7a8e0119307305fa4cfd15281871f1c852787d3f6c1ba3d0bc2342c421bf762', 'Actual V8 baseline changed')
    geometry = load(directory/'geometry.json')
    sprites = manifest['sprites']
    need(sprites == load(directory/'output/registration.json'), 'Final output registration does not match manifest')
    previous_sprites = load(source_root/'attempt-01/registration.json')
    need(len(sprites) == len(previous_sprites) == 53, 'Frozen first/final source census')
    for sprite,previous in zip(sprites,previous_sprites):
        need({k:v for k,v in sprite.items() if k != 'image'} == {k:v for k,v in previous.items() if k != 'image'}, 'Material correction changed first source geometry/registration')
    with Image.open(frozen/'plan/material-ids.png') as ids:
        normalized = validate_geometry(geometry,sprites,ids,load(frozen/'plan/plan.json')['props'])
    sources=[]
    for sprite,item in zip(sprites,normalized):
        image_path=dependency(sprite['image'],root)
        need(directory in image_path.parents and files.get(str(image_path.relative_to(directory))) == sprite['image']['sha256'], 'Supplement image outside manifest')
        with Image.open(image_path) as image:
            need(image.format == 'PNG' and image.mode == 'RGBA' and list(image.size) == item['registration']['canvasPixels'], 'Supplement PNG/canvas format drift')
            image.verify()
        sources.append(dict(file=item['file'],image=sprite['image']))
    # Hash all dependencies on every call. Cache only replay of those exact bytes.
    cache_key=json.dumps(binding,sort_keys=True)
    if cache_key not in _VERIFIED:
        oracle=module('_v9_source_validator',directory/'test_source.py')
        oracle.verify_manifest(path=path,replay=True)
        _VERIFIED.add(cache_key)
    return dict(supplements=normalized,sources=sources)
