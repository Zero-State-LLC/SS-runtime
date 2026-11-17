#!/usr/bin/env python3
"""Render frozen kiosk meshes with retained V9 materials, never overwrite evidence.
ADAPT kiosk/replay.py:99-170 and baseline_renderer.py:17-30,82-144.
Only roof-vent anchor Z follows the already-authored roof surface change.
"""
import argparse
import copy
import hashlib
import importlib.util
import json
from pathlib import Path
import sys
from PIL import Image, ImageDraw

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
PACKET = HERE.parents[1]
ROOT = HERE.parents[4]
OLD = ROOT / 'docs/review/building-perspective-detail-20261116/kiosk'
EDITABLE_SHA = '463ab0139b2316dfe935812cca5aad64c114db8682c76900268d36638d1c110a'
SOURCE_SHA = 'ea13512b2db1cf0975c7daf386c38ce3aa5a1eb0ffc6c1f5da4a4f6bdbb67b1d'


def need(condition, message):
    if not condition:
        raise ValueError(message)


def load(path):
    return json.loads(path.read_text())


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def dump(path, value):
    path.write_text(json.dumps(value, indent=2) + '\n')


def module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    result = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(result)
    return result


base = module('textured_kiosk_retained_base', OLD / 'baseline_renderer.py')
previous = sys.modules.get('baseline_renderer')
sys.modules['baseline_renderer'] = base
try:
    replay = module('textured_kiosk_retained_replay', OLD / 'replay.py')
finally:
    if previous is None:
        del sys.modules['baseline_renderer']
    else:
        sys.modules['baseline_renderer'] = previous


def inputs():
    editable = PACKET / 'editable'
    need(sha(editable / 'manifest.json') == EDITABLE_SHA, 'Editable manifest drift')
    need(sha(PACKET / 'output/manifest.json') == SOURCE_SHA, 'Flat source manifest drift')
    manifest = load(editable / 'manifest.json')
    for name, digest in manifest['outputs'].items():
        need(sha(editable / name) == digest, 'Frozen editable output drift: ' + name)
    mapping = dict(load(PACKET / 'z-map.json')['anchors'])
    need(sha(PACKET / 'z-map.json') == manifest['zMapSHA256'], 'Z map drift')
    current = load(editable / 'current-indexed-mesh.json')
    candidate = load(editable / 'candidate-indexed-mesh.json')
    need(current == load(OLD / 'output/mesh.json'), 'Current mesh differs from retained V9')
    validate_geometry(current, candidate, mapping)
    need(load(OLD / 'geometry-controls.json')['roofZ'] == 125 and mapping[125] == 100, 'Declared roof plane changed')
    paths = [editable / 'manifest.json', editable / 'current-indexed-mesh.json', editable / 'candidate-indexed-mesh.json',
             PACKET / 'output/manifest.json', PACKET / 'z-map.json', HERE / 'build.py', HERE / 'DESIGN.md']
    paths += [OLD / p for p in ['baseline_renderer.py', 'replay.py', 'materials.json', 'roof-layer.json',
                                'geometry-controls.json', 'output/mesh.json', 'output/building-alpha.png',
                                'output/source-full.png', 'output/roof-layer-alpha.png',
                                'inputs/atlas.png', 'inputs/provider.json', 'inputs/benchmark.png',
                                'inputs/roof-vent.png', 'inputs/roof-vent-provider.json']]
    for path in paths:
        need(path.is_file() and path.resolve() == path, 'Missing or aliased dependency: ' + str(path))
    return current, candidate, mapping, {str(p.relative_to(ROOT)): sha(p) for p in paths}


def validate_geometry(current, candidate, mapping):
    need(len(current['vertices']) == len(candidate['vertices']) == 6330, 'Vertex census drift')
    need(current['faces'] == candidate['faces'] and len(current['faces']) == 1582, 'Topology, UV or material drift')
    expected = copy.deepcopy(current)
    expected['height'] = mapping[current['height']]
    for vertex in expected['vertices']:
        vertex[2] = mapping[vertex[2]]
    need(candidate == expected, 'Candidate is not the exact frozen Z-only geometry')


def roof_spec(arm, mapping):
    roof = copy.deepcopy(load(OLD / 'roof-layer.json'))
    roof['localWorldAnchor'][2] = 125 if arm == 'current' else mapping[125]
    return roof


def registration(mesh):
    reg = base.registration(mesh)
    reg.update(canvasPixels=reg['sourceCanvas'], rootPixelsTopLeft=reg['sourceRoot'],
               worldPosition=[512, 640], drawSizeWorld=[v / 5 for v in reg['sourceCanvas']],
               status='TEXTURED_KIOSK_REVIEW_CANDIDATE_NOT_ACCEPTED')
    return replay.add_ground_boundary(reg)


def rgba_equal(image, path):
    with Image.open(path) as reference:
        reference = reference.convert('RGBA')
        return image.size == reference.size and image.tobytes() == reference.tobytes()


def build(output):
    need(not output.exists(), 'Preserve prior textured evidence. Use a new output directory.')
    current, candidate, mapping, dependencies = inputs()
    output.mkdir(parents=True)
    materials = load(OLD / 'materials.json')
    textures = base.textures(materials)
    previews = {}
    bindings = {}
    for arm, mesh in [('current', current), ('candidate', candidate)]:
        directory = output / arm
        directory.mkdir()
        reg = registration(mesh)
        roof = roof_spec(arm, mapping)
        image = replay.render(mesh, textures)
        layer = base.render_roof_layer(roof, reg)
        full = Image.alpha_composite(image, layer)
        if arm == 'current':
            for actual, name in [(image, 'building-alpha.png'), (layer, 'roof-layer-alpha.png'), (full, 'source-full.png')]:
                need(rgba_equal(actual, OLD / 'output' / name), 'Retained V9 RGBA reproduction failed: ' + name)
        image.save(directory / 'building-alpha.png')
        layer.save(directory / 'roof-layer-alpha.png')
        full.save(directory / 'source-full.png')
        dump(directory / 'registration.json', reg)
        dump(directory / 'roof-spec.json', roof)
        dump(directory / 'roof-layer-registration.json', base.roof_layer_registration(roof, reg))
        native = full.resize(tuple(round(v) for v in reg['drawSizeWorld']), Image.Resampling.LANCZOS)
        native.save(directory / 'logical-source.png')
        full.resize(tuple(round(v / 2) for v in reg['drawSizeWorld']), Image.Resampling.LANCZOS).save(directory / 'half-logical-source.png')
        previews[arm] = native
        bindings[arm] = dict(sourceFile=arm + '/source-full.png', sourceSHA256=sha(directory / 'source-full.png'),
                             meshSHA256=sha(PACKET / 'editable' / ('current-indexed-mesh.json' if arm == 'current' else 'candidate-indexed-mesh.json')),
                             registration={key: reg[key] for key in ['canvasPixels', 'rootPixelsTopLeft', 'worldPosition', 'drawSizeWorld', 'groundPixelsTopLeft']},
                             roofAnchor=roof['localWorldAnchor'])
        print('Rendered retained-material kiosk:', arm, full.size, flush=True)
    plate = Image.new('RGB', (1500, 600), '#303536')
    with Image.open(OLD / 'inputs/benchmark.png') as source:
        reference = source.convert('RGB')
        reference.thumbnail((850, 520), Image.Resampling.LANCZOS)
        plate.paste(reference, (0, 45))
    draw = ImageDraw.Draw(plate)
    draw.text((12, 12), 'FULL ORIGINAL BENCHMARK / UNCROPPED', fill='white')
    for arm, x in [('current', 900), ('candidate', 1200)]:
        image = previews[arm]
        plate.paste(image, (x, 130), image)
        draw.text((x, 80), arm.upper() + ' RETAINED MATERIAL', fill='white')
    draw.text((12, 575), 'SOURCE PREVIEW ONLY / NOT NATIVE CAPTURE / unchanged UVs and XY / candidate roof vent follows roof Z125 to100 / NOT ACCEPTED', fill='white')
    plate.save(output / 'source-comparison.png')
    dump(output / 'bindings.json', bindings)
    dump(output / 'manifest.json', dict(schema='kiosk-preserved-material-001', status='TEXTURED_SOURCE_NOT_NATIVE_EVIDENCE',
         ownerAcceptance=False, productionAdmitted=False, inputs=dependencies,
         outputs={str(p.relative_to(output)): sha(p) for p in sorted(output.rglob('*')) if p.is_file()},
         unchangedCurrentRGBAMatches=3, candidateMeshSHA256=bindings['candidate']['meshSHA256']))
    print('Textured manifest SHA256', sha(output / 'manifest.json'), flush=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, default=HERE / 'output')
    args = parser.parse_args()
    build(args.output)
