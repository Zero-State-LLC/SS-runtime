"""Explicit V8 source contract adapter and independent native contact checks.
Source recommendations are consumed, never authored. No source/native output writes.
"""
import hashlib
import importlib.util
import json
import math
import os
from pathlib import Path
import tempfile
import sys
from contextlib import contextmanager
from PIL import Image

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
PLAN = HERE.parent / 'plan'
V7 = HERE.parent.parent / 'building-perspective-detail-20261116/scene'
BASELINE_SHA = '9728f0a030020dff0caad52e8d3791be092a3b6ada8b5ffd845ee9d370785889'
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


@contextmanager
def module_alias(name, value):
    """Resolve the reviewed sibling import without altering source or sys.path."""
    existed, previous = name in sys.modules, sys.modules.get(name)
    sys.modules[name] = value
    try:
        yield
    finally:
        if existed:
            sys.modules[name] = previous
        else:
            sys.modules.pop(name, None)


def dependency(dep, root):
    need(isinstance(dep, dict) and set(dep) == {'path', 'sha256'}, 'Exact dependency fields required')
    path = dep['path']
    need(isinstance(path, str) and path and not path.startswith('/') and '\\' not in path and
         all(p not in ('', '.', '..') for p in path.split('/')), 'Unsafe dependency path')
    root = root.resolve()
    result = root / path
    need(result.resolve() == result and result.is_file() and sha(result) == dep['sha256'], 'Missing/symlinked/stale dependency: ' + path)
    return result


def validate(binding, root=ROOT):
    need(isinstance(binding, dict) and set(binding) == {'schema', 'plan', 'manifest', 'validator', 'recommendation'}, 'Exact coordinator plan envelope required')
    need(binding['schema'] == 'footprint-ground-recommendations-008', 'Unknown plan recommendation version')
    root = root.resolve()
    directory = root / PLAN.relative_to(ROOT)
    paths = {key: dependency(binding[key], root) for key in ('plan', 'manifest', 'validator')}
    for key, name in [('plan', 'plan.json'), ('manifest', 'manifest.json'), ('validator', 'test_plan.py')]:
        need(paths[key] == directory / name, 'Wrong exact plan contract path')
    plan, manifest = load(paths['plan']), load(paths['manifest'])
    need(plan.get('schema') == 'footprint-ground-plan-008', 'Unknown semantic plan')
    need(type(plan.get('attempt')) is int and plan['attempt'] in (1, 2), 'Only bounded first/correction source attempts allowed')
    need(type(manifest.get('attempt')) is int and manifest['attempt'] in (1, 2), 'Only first/material correction attempts allowed')
    need(manifest['attempt'] >= plan['attempt'], 'Material attempt cannot precede geometry origin')
    files = manifest.get('files', {})
    required = {'plan.json', 'author.py', 'replay.py', 'ground.png', 'material-ids.png', 'ground.svg', 'v7-immutable-sha256.json'}
    need(isinstance(files, dict) and required <= set(files), 'Missing editable/semantic/rendered source dependencies')
    dependencies = []
    for name, digest in sorted(files.items()):
        need(isinstance(name, str) and not name.startswith('/') and '\\' not in name and all(part not in ('', '.', '..') for part in name.split('/')), 'Manifest path escape')
        dep = dict(path=str((directory / name).relative_to(root)), sha256=digest)
        dependency(dep, root)
        dependencies.append(dep)
    need(files['plan.json'] == binding['plan']['sha256'], 'Manifest semantic plan mismatch')
    material_spec = None
    if manifest['attempt'] == 2:
        need({'materials.json', 'material.py', 'attempt-01/plan.json', 'attempt-01/material-ids.png'} <= set(files), 'Missing bounded material correction dependencies')
        material_spec = load(directory / 'materials.json')
        need(material_spec.get('schema') == 'bounded-material-correction-002' and material_spec.get('attempt') == material_spec.get('maximumAttempts') == 2, 'Unknown material correction')
        need(material_spec.get('sharedPlanSHA256') == binding['plan']['sha256'] == files['attempt-01/plan.json'], 'Correction changed geometry origin plan')
        need(files['material-ids.png'] == files['attempt-01/material-ids.png'], 'Material correction changed semantic ground geometry')
        for key in ('retainedPaving', 'retainedOriginal'):
            dependency(material_spec[key], root)
            dependencies.append(material_spec[key])
    rec = binding['recommendation']
    need(isinstance(rec, dict) and set(rec) == {'reviewerRole', 'decision', 'scope', 'planSHA256', 'sourceSHA256', 'evidence'}, 'Exact coordinator recommendation required')
    need(rec['reviewerRole'] == 'coordinator' and rec['decision'] == 'recommended' and rec['scope'] == 'isolated-ordinary-scene', 'Source not coordinator recommended')
    need(rec['planSHA256'] == binding['plan']['sha256'] and rec['sourceSHA256'] == files['ground.png'], 'Stale/forged semantic/source recommendation')
    dependency(rec['evidence'], root)
    previous_path = root / V7.relative_to(ROOT) / 'native-capture-v7/source-scene-records.json'
    need(sha(previous_path) == BASELINE_SHA, 'Frozen V7 authority drift')
    previous = next(c for c in load(previous_path)['captures'] if c['arm'] == 'candidate' and c['zoom'] == 1)
    expected_protected = {key: previous[key] for key in ['solids', 'cameraRoot', 'cameraFieldOrigin', 'cameraFieldAngleMilli', 'cameraHeadingMilli', 'cameraRange', 'centerWorld', 'controlsRetained']}
    expected_protected['actors'] = [a for a in previous['preprojectionInventory'] if not a['name'].startswith('benchmark-prop-')]
    need(plan.get('protected') == expected_protected, 'Forged protected authority/actor fields')
    need(plan.get('arenaClipWorld') == [0, 0, 2304, 1536], 'Ground coverage changed')
    need(plan.get('materialIDs') == dict(road=1, curb=2, sidewalk=3, foundation=4), 'Unknown semantic material IDs')
    need(plan['outputs']['ground'] == 'ground.png' and plan['outputs']['materialIDs'] == 'material-ids.png' and plan['outputs']['editable'] == 'ground.svg', 'Wrong output bindings')
    actors = {a['name']: a for a in previous['actors']}
    need([p['name'] for p in plan['props']] == ['benchmark-prop-0', 'benchmark-prop-1'], 'Wrong prop census')
    for prop in plan['props']:
        need(prop['oldWorldRoot'] == actors[prop['name']]['worldRoot'], 'Forged baseline prop root')
        need(prop['sourceArt'] == 'unchanged' and prop['groundMaterial'] == 'sidewalk', 'Prop source/treatment outside scope')
        need(all(type(v) in (int, float) and math.isfinite(v) for v in prop['worldRoot']) and len(prop['worldRoot']) == 2, 'Invalid prop root')
    # Always rehash every source. Cache only deterministic replay of those exact bytes.
    cache_key = json.dumps(binding, sort_keys=True) + json.dumps(files, sort_keys=True)
    if cache_key not in _VERIFIED:
        oracle = module('_v8_source_semantics', paths['validator'])
        with Image.open(directory / 'material-ids.png') as ids:
            need(ids.mode == 'L', 'Semantic image must be raw material IDs')
            oracle.validate(plan, ids)
            if material_spec is not None:
                with Image.open(directory / 'road-details.png') as details:
                    oracle.validate_details(plan, ids, details)
        with Image.open(directory / 'ground.png') as image:
            need(image.format == 'PNG' and image.mode == 'RGB' and image.size == (4608, 4608), 'Ground raster registration/mode')
            oracle.validate_ground_pixels(plan, image)
        with tempfile.TemporaryDirectory(prefix='v8-plan-replay-', dir=os.environ.get('JCODE_SCRATCH_DIR')) as temp:
            temporary = Path(temp)
            (temporary / 'plan.json').write_bytes(paths['plan'].read_bytes())
            if material_spec is not None:
                (temporary / 'materials.json').write_bytes((directory / 'materials.json').read_bytes())
                material = module('_v8_material_replay', directory / 'material.py')
                material.HERE, material.ROOT = temporary, root
                with module_alias('material', material):
                    replay = module('_v8_source_replay', directory / 'replay.py')
                replay.HERE = temporary
                outputs = ['ground.png', 'material-ids.png', 'ground.svg', 'road-details.png', 'road-details-mask.png',
                           'road-mask.png', 'road-details.svg-fragment', 'final-plan-preview.png', 'final-source-detail.png'] + [f'material-{i}-tile.png' for i in range(1, 5)]
            else:
                replay = module('_v8_source_replay', directory / 'replay.py')
                replay.HERE = temporary
                outputs = ['ground.png', 'material-ids.png', 'ground.svg']
            replay.main()
            for name in outputs:
                need(name in files and sha(temporary / name) == files[name], 'Rendered source not deterministic semantic plan output: ' + name)
        _VERIFIED.add(cache_key)
    source = dict(role='ground-plan', status='recommended',
                  image=dict(path=str((directory / 'ground.png').relative_to(root)), sha256=files['ground.png']),
                  registration=plan['registration'], dependencies=dependencies + [binding['manifest'], binding['validator']],
                  recommendation=dict(reviewerRole=rec['reviewerRole'], decision=rec['decision'], scope=rec['scope'],
                                      sourceSHA256=rec['sourceSHA256'], evidence=rec['evidence']))
    return dict(source=source, planSHA256=binding['plan']['sha256'], scenePlan={key: plan[key] for key in ('props', 'buildings')})


def close(actual, expected, label):
    if isinstance(expected, list):
        need(isinstance(actual, list) and len(actual) == len(expected), 'Missing ' + label)
        for observed, wanted in zip(actual, expected):
            close(observed, wanted, label)
    else:
        need(type(actual) in (int, float) and math.isfinite(actual) and abs(actual - expected) <= .002, 'Wrong ' + label)


def projected(point, row):
    x, y = [point[i] - row['centerWorld'][i] for i in range(2)]
    delta = [(x - y) / math.sqrt(2), (x + y) / (2 * math.sqrt(2))]
    return [row['centerWorld'][i] + row['zoom'] * delta[i] for i in range(2)]


def in_crop(point, row):
    c = row['centerWorld']
    return c[0] - 352 <= point[0] < c[0] + 352 and c[1] - 163 <= point[1] < c[1] + 163


def contact_expected(row, prepared):
    bindings = {b['nodeName']: b for b in prepared['buildings']}
    sources = {s['role']: s for s in prepared['sources']}
    plans = {b['id']: b for b in prepared['scenePlan']['buildings']}
    result = []
    for actor in row['actors']:
        if actor['name'] not in row['buildingSourceSHA256']:
            continue
        w, h = [actor['size'][i] * actor['scale'][i] * row['zoom'] for i in range(2)]
        x = actor['projectedRoot'][0] - actor['anchor'][0] * w
        y = actor['projectedRoot'][1] - actor['anchor'][1] * h
        cx, cy = row['centerWorld']
        if not (x < cx + 352 and x + w > cx - 352 and y < cy + 163 and y + h > cy - 163):
            continue
        need(actor['name'] in bindings, 'Visible building lacks actual contact source')
        binding = bindings[actor['name']]
        plan = plans[binding['solidID']]
        source = sources[binding['role']]
        reg = source['registration']
        need(plan['meshContactStatus'] == 'actual-z0-face-vertices' and len(plan['contactLandmarks']) >= 3, 'Actual visible contact required')
        need(plan['actualContactWorld'] == [p['world'] for p in plan['contactLandmarks']], 'Contour/landmark mismatch')
        landmarks = []
        for landmark in plan['contactLandmarks']:
            need(landmark['provenance'] == 'actual-z0-mesh-vertex', 'Virtual corner is not visible mesh contact')
            pixel = landmark['sourcePixelsTopLeft']
            local = [(pixel[0] - reg['rootPixelsTopLeft'][0]) * reg['drawSizeWorld'][0] / reg['canvasPixels'][0],
                     (reg['rootPixelsTopLeft'][1] - pixel[1]) * reg['drawSizeWorld'][1] / reg['canvasPixels'][1]]
            actual = [actor['projectedRoot'][i] + local[i] * actor['scale'][i] * row['zoom'] for i in range(2)]
            ground = projected(landmark['world'], row)
            close(actual, ground, 'actual mesh source-to-ground contact')
            landmarks.append(dict(**landmark, projectedSource=actual, projectedGround=ground, inCrop=in_crop(actual, row)))
        result.append(dict(nodeName=actor['name'], solidID=binding['solidID'], sourceSHA256=source['sha256'],
                           canvasIntersectsCrop=True, meshContactStatus=plan['meshContactStatus'], landmarks=landmarks))
    need(len(result) == 5, 'Exact five visible building contact witnesses required')
    return result


def witnesses_expected(row, prepared):
    contacts = contact_expected(row, prepared)
    candidate = row['arm'] == 'candidate'
    role = 'ground-plan' if candidate else 'paving'
    source = next(s for s in prepared['sources'] if s['role'] == role)
    corners = [[0, 0], [2304, 0], [2304, 1536], [0, 1536]]
    ground = dict(nodeName='benchmark-ground-patch-0', sourceRole=role, sourceSHA256=source['sha256'], planApplied=candidate,
                  size=[2304, 1536], anchor=[.5, .5], zPosition=.1, alpha=1, hidden=False,
                  worldCorners=corners, projectedCorners=[projected(p, row) for p in corners])
    props = []
    for prop in prepared['scenePlan']['props']:
        root = prop['worldRoot'] if candidate else prop['oldWorldRoot']
        props.append(dict(nodeName=prop['name'], worldRoot=root, projectedRoot=projected(root, row), planApplied=candidate,
                          contactRadiusWorld=prop['contactRadiusWorld'], shadowRadiusWorld=prop['shadowRadiusWorld'],
                          shadowAlphaMax=prop['shadowAlphaMax'], limitsMeaning='candidate-baked-ground-plan-limits-not-measured-sprite-alpha'))
    return dict(visibleBuildingContacts=contacts, groundPlanWitness=ground, propPlanWitnesses=props)


def exact_tree(actual, expected, label):
    if isinstance(expected, dict):
        need(isinstance(actual, dict) and set(actual) == set(expected), 'Wrong exact ' + label + ' fields')
        for key in expected:
            exact_tree(actual[key], expected[key], label + '/' + key)
    elif isinstance(expected, list):
        need(isinstance(actual, list) and len(actual) == len(expected), 'Wrong ' + label + ' census')
        for observed, wanted in zip(actual, expected):
            exact_tree(observed, wanted, label)
    elif type(expected) in (int, float):
        close(actual, expected, label)
    else:
        need(type(actual) is type(expected) and actual == expected, 'Wrong ' + label)


def validate_contacts(row, prepared):
    for key, expected in witnesses_expected(row, prepared).items():
        exact_tree(row.get(key), expected, key)
