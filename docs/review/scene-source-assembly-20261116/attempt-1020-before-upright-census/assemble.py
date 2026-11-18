#!/usr/bin/env python3
"""Review-only, fail-closed source assembly. Never a native/game capture."""
import argparse
import base64
import hashlib
import json
import math
from pathlib import Path, PurePosixPath
import shutil
import subprocess
import sys
from PIL import Image

HERE = Path(__file__).resolve().parent
ROLES = {'paving', 'camera', 'player', 'stone'}
SCHEMA = 'scene-source-assembly-001'
LABEL = 'OFFLINE SOURCE ASSEMBLY - NOT NATIVE / NOT ACCEPTED'


class Invalid(ValueError):
    pass


def need(condition, message):
    if not condition:
        raise Invalid(message)


def digest(data):
    return hashlib.sha256(data).hexdigest()


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':'), allow_nan=False).encode()


def safe(root, name):
    need(isinstance(name, str) and bool(name), 'Missing dependency path')
    p = PurePosixPath(name)
    need(not p.is_absolute() and '\\' not in name and all(x not in ('', '.', '..') for x in name.split('/')), 'Path escape/alias: ' + name)
    target = root / name
    need(target.resolve().is_relative_to(root.resolve()), 'Symlink path escape: ' + name)
    # Internal symlinks also conceal actual dependency identities.
    need(not any((root / Path(*p.parts[:i])).is_symlink() for i in range(1, len(p.parts) + 1)), 'Symlink dependency: ' + name)
    return target


def tracking(root):
    if (root / '.git').exists():
        names = subprocess.check_output(['git', '-C', str(root), 'ls-files', '-z']).decode().split('\0')
        return {name: None for name in names if name}
    record = root / 'tracked-inputs.json'
    need(record.is_file(), 'No Git tracking or explicit exported tracking receipt')
    data = json.loads(record.read_text())
    need(data.get('schema') == 'tracked-scene-inputs-001', 'Unknown tracking receipt')
    need(isinstance(data.get('gitHead'), str) and len(data['gitHead']) == 40, 'Missing export origin')
    files = data.get('files')
    need(isinstance(files, dict) and bool(files), 'Missing export dependency inventory')
    for name, sha in files.items():
        safe(root, name)
        need(isinstance(sha, str) and len(sha) == 64 and all(c in '0123456789abcdef' for c in sha), 'Invalid export dependency digest')
    return files


def dependency(root, record, tracked):
    need(isinstance(record, dict), 'Missing explicit dependency record')
    name = record.get('path')
    path = safe(root, name)
    need(name in tracked, 'Untracked dependency: ' + name)
    need(path.is_file(), 'Missing dependency: ' + name)
    data = path.read_bytes()
    sha = digest(data)
    need(record.get('sha256') == sha, 'Dependency hash mismatch: ' + name)
    need(tracked[name] is None or tracked[name] == sha, 'Export receipt mismatch: ' + name)
    return data


def pair(value, label, positive=False):
    need(isinstance(value, list) and len(value) == 2 and all(type(v) in (int, float) and math.isfinite(v) for v in value), 'Invalid ' + label)
    need(not positive or all(v > 0 for v in value), 'Nonpositive ' + label)
    return value


def validate(manifest, root):
    need(manifest.get('schema') == SCHEMA, 'Unknown assembly version')
    need(manifest.get('evidenceKind') == 'OFFLINE_REVIEW_ONLY', 'Invalid evidence claim')
    need(manifest.get('gameplayAuthority') == 'NONE_COLLISION_AND_FIELDS_UNCHANGED', 'Gameplay authority forbidden')
    need(manifest.get('projection') == 'D108_X_MINUS_Y_Y_PLUS_X_HALF', 'Unknown projection')
    pair(manifest.get('viewCenterWorld'), 'view center')
    need(type(manifest.get('pixelsPerWorldUnit')) in (int, float) and math.isfinite(manifest['pixelsPerWorldUnit']) and 0 < manifest['pixelsPerWorldUnit'] <= 16, 'Invalid viewport scale')
    canvas = pair(manifest.get('canvasPixels'), 'canvas', True)
    need(all(type(v) is int and v <= 8192 for v in canvas), 'Invalid canvas dimensions')
    sources = manifest.get('sources')
    need(isinstance(sources, list) and len(sources) == 4 and {s.get('role') for s in sources} == ROLES, 'Exactly paving/camera/player/stone required')
    tracked = tracking(root)
    deps = []
    for record in manifest.get('contextDependencies', []):
        dependency(root, record, tracked)
        deps.append(record)
    blockers = []
    for source in sources:
        role = source['role']
        status = source.get('status')
        need(status in ('pending', 'rejected', 'recommended'), 'Unknown source status: ' + role)
        if status != 'recommended':
            need(all(source.get(k) is None for k in ('image', 'registration', 'recommendation')), 'Pending/rejected source must not carry admitted art: ' + role)
            need(isinstance(source.get('reason'), str) and bool(source['reason'].strip()), 'Missing blocking reason: ' + role)
            blockers.append(role + ': ' + source['reason'])
            continue
        raw = dependency(root, source.get('image'), tracked)
        deps.append(source['image'])
        import io
        with Image.open(io.BytesIO(raw)) as image:
            need(image.format == 'PNG', 'Source must be PNG: ' + role)
            size = list(image.size)
            image.verify()
        reg = source.get('registration')
        need(isinstance(reg, dict), 'Missing registration: ' + role)
        need(reg.get('canvasPixels') == size, 'Source dimensions mismatch: ' + role)
        anchor = pair(reg.get('rootPixelsTopLeft'), 'source root')
        need(all(0 <= v <= bound for v, bound in zip(anchor, size)), 'Root outside source canvas')
        pair(reg.get('worldPosition'), 'world placement')
        pair(reg.get('drawSizeWorld'), 'world size', True)
        need(reg.get('kind') == ('ground' if role == 'paving' else 'upright'), 'Wrong registration kind')
        need(reg.get('coordinates') == 'WORLD_X_RIGHT_Y_UP_SOURCE_TOP_LEFT', 'Missing coordinate convention')
        recommendation = source.get('recommendation')
        need(isinstance(recommendation, dict), 'Missing coordinator recommendation: ' + role)
        need(recommendation.get('reviewerRole') == 'coordinator' and recommendation.get('decision') == 'recommended', 'Coordinator recommendation required: ' + role)
        need(recommendation.get('scope') == ('bounded-material-layout' if role == 'paving' else 'isolated-ordinary-scene'), 'Wrong recommendation scope: ' + role)
        need(recommendation.get('sourceSHA256') == source['image']['sha256'], 'Stale recommendation source: ' + role)
        need(recommendation.get('registrationSHA256') == digest(canonical(reg)), 'Stale recommendation registration: ' + role)
        evidence = recommendation.get('evidence')
        dependency(root, evidence, tracked)
        deps.append(evidence)
    need(len({r['path'] for r in deps}) > 0, 'No context inputs')
    return blockers, deps


def project(point):
    x, y = point
    return ((x - y) / math.sqrt(2), (x + y) / (2 * math.sqrt(2)))


def render(manifest, root, output):
    blockers, _ = validate(manifest, root)
    need(not blockers, 'BLOCKED: ' + ' | '.join(blockers))
    # Read verified bytes again only in this process. No source-derived collision/fields.
    tracked = tracking(root)
    width, height = manifest['canvasPixels']
    scale = manifest['pixelsPerWorldUnit']
    cx, cy = project(manifest['viewCenterWorld'])
    parts = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">', '<rect width="100%" height="100%" fill="#242424"/>']
    sources = sorted(manifest['sources'], key=lambda s: (s['role'] != 'paving', -sum(s['registration']['worldPosition']), s['role']))
    for source in sources:
        reg = source['registration']
        w, h = reg['canvasPixels']
        rw, rh = reg['drawSizeWorld']
        ax, ay = reg['rootPixelsTopLeft']
        px, py = project(reg['worldPosition'])
        tx, ty = width / 2 + scale * (px - cx), height / 2 - scale * (py - cy)
        if reg['kind'] == 'upright':
            a, b, c, d = scale * rw / w, 0, 0, scale * rh / h
        else:
            # Source rows advance downward, opposite world +Y.
            a = scale * rw / w / math.sqrt(2)
            b = -a / 2
            c = scale * rh / h / math.sqrt(2)
            d = c / 2
        tx -= a * ax + c * ay
        ty -= b * ax + d * ay
        encoded = base64.b64encode(dependency(root, source['image'], tracked)).decode()
        parts.append(f'<image width="{w}" height="{h}" transform="matrix({a} {b} {c} {d} {tx} {ty})" href="data:image/png;base64,{encoded}"/>')
    parts.append(f'<rect width="100%" height="24" fill="black"/><text x="8" y="17" fill="white" font-size="12">{LABEL}</text></svg>')
    # Exclusive creation preserves prior evidence and cannot overwrite inputs.
    with Path(output).open('x') as stream:
        stream.write('\n'.join(parts) + '\n')


def export_packet(manifest, root, output):
    _, deps = validate(manifest, root)
    need((root / '.git').exists(), 'Export requires Git provenance')
    output = Path(output)
    need(not output.exists(), 'Export destination already exists')
    output.mkdir(parents=True)
    inventory = {}
    for record in deps:
        name = record['path']
        dest = safe(output, name)
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(safe(root, name), dest)
        inventory[name] = record['sha256']
    (output / 'assembly.json').write_text(json.dumps(manifest, indent=2) + '\n')
    shutil.copyfile(Path(__file__), output / 'assemble.py')
    head = subprocess.check_output(['git', '-C', str(root), 'rev-parse', 'HEAD'], text=True).strip()
    (output / 'tracked-inputs.json').write_text(json.dumps({'schema': 'tracked-scene-inputs-001', 'gitHead': head, 'files': inventory}, indent=2) + '\n')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, required=True, help='Repository root or exported packet root')
    parser.add_argument('--manifest', type=Path, default=HERE / 'assembly.json')
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument('--render', type=Path, help='New offline SVG file, only when all inputs admitted')
    mode.add_argument('--export', type=Path, help='New portable packet directory, permitted while blocked')
    args = parser.parse_args()
    try:
        manifest = json.loads(args.manifest.read_text())
        blockers, _ = validate(manifest, args.root.resolve())
        if args.render:
            render(manifest, args.root.resolve(), args.render)
        if args.export:
            export_packet(manifest, args.root.resolve(), args.export)
        print(json.dumps({'status': 'BLOCKED_NO_SCENE' if blockers else 'READY_OFFLINE_ONLY', 'blockers': blockers, 'nativeEvidence': False, 'ownerAcceptance': False}, indent=2))
        return 2 if blockers else 0
    except (Invalid, OSError, ValueError, KeyError, TypeError) as error:
        print('INVALID: ' + str(error), file=sys.stderr)
        return 1


if __name__ == '__main__':
    sys.exit(main())
