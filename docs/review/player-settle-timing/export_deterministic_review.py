"""Export explicitly timed native renderer attachments; never label as live video."""
import hashlib
import json
from pathlib import Path
import re
import shutil
import subprocess
import sys

source, target = map(Path, sys.argv[1:3])
target.mkdir(parents=True, exist_ok=True)
manifest = json.loads((source / 'manifest.json').read_text())
images, traces = {}, {}
for case in manifest:
    for a in case['attachments']:
        name = a.get('suggestedHumanReadableName', '')
        path = source / a['exportedFileName']
        m = re.search(r'deterministic-stop-(\d+)-reduced-(true|false)-sample-(\d+)', name)
        if m:
            key = (int(m[1]), m[2], int(m[3]))
            assert key not in images
            images[key] = path
        elif 'records' in name and path.suffix == '.json':
            rows = json.loads(path.read_text())
            if rows and rows[0].get('evidenceKind', '').startswith('explicit-time'):
                key = (rows[0]['releaseTargetFrame'] + 1, str(rows[0]['reducedMotion']).lower())
                assert key not in traces
                traces[key] = rows
assert set(traces) == {(p, r) for p in (5, 13) for r in ('true', 'false')}
checks = []
for (phase, reduced), rows in sorted(traces.items()):
    name = f'stop-{phase:02d}-reduced-{reduced}'
    folder = target / name
    folder.mkdir(exist_ok=True)
    samples = sorted(k[2] for k in images if k[:2] == (phase, reduced))
    assert samples == list(range(len(samples)))
    assert len(rows) == len(samples), (len(rows), len(samples))
    assert rows[-1]['tick'] == 165
    assert rows[-1]['requestedClip'] == 'player_idle'
    settling = sorted({r['settleFrame'] for r in rows if r['settleFrame'] >= 0})
    assert settling == ([] if reduced == 'true' else list(range(17)))
    moving = [r['frame'] for r in rows if r['requestedClip'] == 'player_move']
    assert set(moving) == set(range(16))
    assert any(a == 15 and b == 0 for a, b in zip(moving, moving[1:])), 'walk seam absent'
    for sample, row in enumerate(rows):
        assert row['exportSample'] == sample
        assert abs(row['exportTime'] - sample / 60) < 1e-9
        src = images[(phase, reduced, sample)]
        dst = folder / f'{sample:03d}.png'
        shutil.copy2(src, dst)
        row['imageSHA256'] = hashlib.sha256(src.read_bytes()).hexdigest()
    (folder / 'frames.json').write_text(json.dumps(rows, indent=2))
    for label, rate in [('normal', 60), ('quarter', 15)]:
        subprocess.run(['/opt/homebrew/bin/ffmpeg', '-v', 'error', '-y', '-framerate', str(rate),
            '-i', str(folder / '%03d.png'), '-c:v', 'libx264', '-crf', '16', '-pix_fmt', 'yuv420p',
            '-movflags', '+faststart', str(target / f'{name}-{label}.mp4')], check=True)
    checks.append({'phase': phase, 'reducedMotion': reduced, 'samples': len(samples),
        'settlePoses': settling, 'walkSeamPresent': True, 'finalTick': rows[-1]['tick']})
for label, title in [('normal', 'Normal speed'), ('quarter', 'Quarter speed')]:
    cards = ''.join(f'<section><h2>Release {p} · {"Reduced Motion" if r == "true" else "Standard"}</h2>'
        f'<video controls muted playsinline preload="metadata" src="stop-{p:02d}-reduced-{r}-{label}.mp4"></video></section>'
        for p in (5, 13) for r in ('false', 'true'))
    other = 'quarter' if label == 'normal' else 'normal'
    (target / f'{label}-speed.html').write_text(f'''<!doctype html><meta charset="utf-8"><title>{title} · native renderer export</title>
<style>body{{font:17px system-ui;background:#171a1d;color:#eee;margin:32px;max-width:1000px}}a{{color:#a5d8ff}}p{{line-height:1.5}}video{{width:100%;max-width:704px}}section{{margin:32px 0}}</style>
<h1>{title}</h1><p>0.375-second settle · narrow stance and opposing arm swing · complete walk cycles, stop and held idle.</p>
<p>Explicit-time SpriteKit renderer export. This shows authored motion and composition; it does not prove live display cadence. {"Quarter speed stretches the same rendered frames fourfold; no interpolated frames." if label == "quarter" else "Review weight transfer and overall motion here. Inspect detail separately at quarter speed."}</p>
<p><a href="{other}-speed.html">Open {other} speed separately</a></p>{cards}''')
(target / 'checks.json').write_text(json.dumps(checks, indent=2))
print(json.dumps(checks, indent=2))
