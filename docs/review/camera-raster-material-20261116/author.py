#!/usr/bin/env python3
"""One-time authoring record. Only writes model/provenance, never alters material pixels."""
import hashlib
import json
from pathlib import Path
from PIL import Image
HERE = Path(__file__).resolve().parent

def dump(path, data):
    path.write_text(json.dumps(data, indent=2) + '\n')

def author():
    prior = json.loads((HERE/'inputs/prior-geometry.json').read_text())
    parts = []
    enamel = {'bracket', 'bracket_neck', 'hood', 'service_box'}
    for i, old in enumerate(prior['parts']):
        name = old['name']
        tint = [54, 55, 53]
        if name in enamel:
            tint = [196, 187, 166]
        if name == 'dome':
            tint = [18, 29, 32]
        if name == 'cyan_lens':
            tint = [46, 222, 213]
        part = dict(name=name, contour=old['contour'], transform=[1, 1, 0, 0],
                    uv=[(i*73)%450, (i*109)%400, 360, 640],
                    tint=tint, material='iron.png', texture_strength=.65 if name not in enamel else .32,
                    shading=dict(ambient=.62, roundness=.55, light_u=.28, vertical=.10),
                    edge=dict(color=[20, 23, 23], width=.65), visible=True)
        # Geometry edits are affine in construction coordinates, not image reshapes.
        if name in {'foot', 'plinth', 'socket', 'ankle_ring'}:
            part['transform'] = [.92, .90, 46*(1-.92), 432*(1-.90)]
        if name in {'hood', 'dome', 'cyan_lens'}:
            part['transform'] = [.95, .85, 116*(1-.95), 118*(1-.85)]
        if name == 'bracket':
            part['contour'] = 'M 53 65 L 64 59 L 70 63 L 70 80 L 103 69 C 109 64 123 61 129 66 L 130 81 C 127 89 116 91 105 87 L 83 94 C 74 99 71 107 71 124 L 63 129 L 53 125 Z'
            part['shading']['roundness'] = .24
        if name == 'bracket_neck':
            part['transform'] = [.88, .84, 117*(1-.88), 76*(1-.84)]
        if name == 'finial':
            part['transform'] = [.94, .94, 45*.06, 29*.06]
        if name == 'cyan_lens':
            part['texture_strength'] = 0
            part['shading'] = dict(ambient=1, roundness=0, light_u=.5, vertical=0)
            part['edge']['width'] = 0
        # Real broad construction faces remain separately editable shading regions.
        part['faces'] = []
        if name in {'bracket', 'service_box', 'foot', 'plinth', 'bracket_neck'}:
            for s, gain in zip(old['surfaces'][:3], [1.08, 1.02, .82]):
                part['faces'].append(dict(name=s['name'], contour=s['path'], gain=gain))
        parts.append(part)
    model = dict(schema=1, status='FIRST_PILOT_REVIEW_ONLY', canvas=prior['canvas'], root=prior['root'],
                 scale=prior['scale'], parts=parts,
                 correctionNotes={
                     'head':'Hood, glass and lens share 0.95x / 0.85y transform about (116,118), reducing bulb depth together.',
                     'bracket':'Re-authored narrow plate and inner return. Neck 0.88x / 0.84y about (117,76).',
                     'base':'Foot, plinth, socket and ankle 0.92x / 0.90y about base (46,432).',
                     'finial':'0.94 uniform about (45,29). Pole axis and source canvas unchanged.',
                     'authority':'Contour corrections are visual hypotheses against unchanged reference, not measured production geometry.'})
    dump(HERE/'model.json', model)
    origins = {
        'prior-geometry.json':'docs/review/camera-surface-authored-20261116/geometry.json',
        'prior-build.py':'docs/review/camera-surface-authored-20261116/build.py',
        'reference.png':'docs/review/camera-surface-authored-20261116/inputs/reference.png',
        'rejected-master.png':'docs/review/camera-surface-authored-20261116/attempt-02/camera-master.png',
        'paving.png':'AppTests/WholeSceneAssets/whole-scene-muted-paving.png'}
    files = {}
    for p in sorted((HERE/'inputs').iterdir()):
        rec = dict(sha256=hashlib.sha256(p.read_bytes()).hexdigest(), bytes=p.stat().st_size,
                   origin=origins.get(p.name, 'supplied image-generation ig_047e2f0bb16e8096016afacdaa899487d0a6456462a8499a29'),
                   role='construction only' if p.name.startswith('prior-') else 'comparison only' if p.name in {'reference.png','rejected-master.png'} else 'background only' if p.name=='paving.png' else 'independent material')
        if p.suffix=='.png':
            with Image.open(p) as im:
                rec.update(size=list(im.size), mode=im.mode, embeddedMetadata=im.info)
        files[p.name] = rec
    dump(HERE/'provenance.json', dict(trackedInputCommit='e90b2361bcd80f4a15dd5c39335b2fc69f7be993', files=files,
        requestedMaterialSize=[1024,1024], actualMaterialSize=[1254,1254],
        materialInspection='Opaque RGB, no embedded PNG metadata. Separate provider JSON retained verbatim. Grey cast-iron field with sparse chips, not benchmark pixels.',
        adapt='ADAPT prior-build.py lines 32-59 cubic path sampling algorithm only. Prior geometry contours and selected broad-face paths are construction inputs, not accepted source. Prior pigments and dab/scratch surfaces not rendered.'))

if __name__ == '__main__':
    author()
