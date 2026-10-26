"""Model-derived support-foot drift from archived current native playback traces.
Not sole-pixel tracking, video synchronization, or a visual pass/fail threshold.
"""
from pathlib import Path
import hashlib
import json

here = Path(__file__).resolve().parent
runtime = here.parents[2]
poses_path = runtime / 'AppTests/BenchmarkAssets/player-source-s-poses.json'
poses = json.loads(poses_path.read_text())
record = json.loads((runtime / 'AppTests/BenchmarkAssets/player-source-s-record.json').read_text())
baseline = json.loads((here.parent / 'player-settle-timing/native-pose-suite-inputs.json').read_text())
for name, expected in record['sourceFiles'].items():
    path = runtime / 'AppTests/BenchmarkAssets' / name
    actual = hashlib.sha256(path.read_bytes()).hexdigest()
    assert actual == expected, name
    if path.suffix == '.png':
        assert actual == baseline[str(path.relative_to(runtime))], name
assert len(poses) == 16
results = []
for folder in sorted([*here.glob('current-*-attachments'), here / 'distance-comparison-attachments']):
    for path in sorted(folder.glob('*.json')):
        records = json.loads(path.read_text())
        if not isinstance(records, list) or not records or not isinstance(records[0], dict) or 'tick' not in records[0]:
            continue
        rows = [r for r in records if r.get('sourceFrameIndex', -1) >= 0 and r.get('clip') == 'player_move|s']
        if not rows:
            continue
        segments = []
        for side in ('left', 'right'):
            active = []
            previous_frame = None
            def finish():
                if len(active) > 1:
                    ys = [r['modelToeY'] for r in active]
                    span = max(ys) - min(ys)
                    segments.append({'side': side, 'startTick': active[0]['tick'], 'endTick': active[-1]['tick'],
                        'observedPoses': sorted({r['pose'] for r in active}), 'sampleCount': len(active),
                        'rangeLogical': span, 'rangeCapturedPixels': span * rows[0]['viewScale'], 'observations': active.copy()})
                active.clear()
            for row in rows:
                frame = row['sourceFrameIndex']
                leg = next(x for x in poses[frame]['legs'] if x['side'] == side)
                if previous_frame is not None and frame < previous_frame:
                    finish()
                previous_frame = frame
                if not leg['contact']:
                    finish()
                    continue
                assert row['groundYScale'] == 0.5 and row['artYScaleAfterParent'] == 1
                assert row['width'] == 64
                # Authored model is already in logical units: six source pixels per unit.
                y = row['renderedY'] - leg['toe'][1] * 0.5 + leg['toe'][2]
                active.append({'tick': row['tick'], 'pose': frame, 'modelToeY': y,
                    'renderedRootY': row['renderedY'], 'authoritativeRawY': row['authoritativeRawY']})
            finish()
        spans = [s['rangeLogical'] for s in segments]
        results.append({'trace': str(path.relative_to(here)), 'sha256': hashlib.sha256(path.read_bytes()).hexdigest(),
            'axis': rows[0]['inputAxis'], 'reducedMotion': rows[0]['reducedMotion'],
            'distancePhaseComparison': rows[0]['distancePhaseComparison'],
            'allObservedPoses': sorted({r['sourceFrameIndex'] for r in rows}),
            'segmentRangeLogical': [min(spans), max(spans)], 'segments': segments})
assert len(results) == 18
output = {'status': 'MEASURED_MODEL_ONLY_NO_ACCEPTANCE_THRESHOLD',
    'sourcePoseSHA256': hashlib.sha256(poses_path.read_bytes()).hexdigest(),
    'sourceIdentity': record['sourceRevision'],
    'method': 'rendered root Y minus authored toe forward times0.5 plus toe height; source-space model, not tracked sole pixels. Retain held-pose movement and missing observations.',
    'results': results}
(here / 'current-contact-audit.json').write_text(json.dumps(output, indent=2) + '\n')
for r in results:
    print(r['axis'], r['reducedMotion'], r['distancePhaseComparison'], r['segmentRangeLogical'], len(r['segments']))
