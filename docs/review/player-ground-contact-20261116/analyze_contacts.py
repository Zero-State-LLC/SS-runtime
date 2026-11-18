#!/usr/bin/env python3
"""Join actual Swift core trace positions to authored exported foot landmarks.
No velocity normalization, collision, world stepping or simplified simulation here.
This is exported-pose sampling, NOT actual displayed/native contact.
"""
import hashlib
import json
import math
from pathlib import Path
HERE = Path(__file__).resolve().parent

def read(name):
    return json.loads((HERE / name).read_text())

def project(x, y):
    return ((x-y)/math.sqrt(2), (x+y)/(2*math.sqrt(2)))

def contact(row, leg):
    x, y = row['xRaw']/256, row['yRaw']/256
    tx, ty, tz = leg['toe']
    if tz != 0:
        raise ValueError('Declared contact above source ground')
    # Source upright pixels /6 at anchor192/336, then ground inverse.
    ox, oy = tx, -.5*ty
    wx = x + (ox + 2*oy)/math.sqrt(2)
    wy = y + (-ox + 2*oy)/math.sqrt(2)
    vx, vy = project(x, y)
    return {'world': [wx, wy], 'viewLogical': [vx+ox, vy+oy],
            'sourcePixels': [192+6*tx, 336+3*ty]}

def analyze(trace, poses, policy):
    distance = 0.0
    result, segments = [], []
    active = {'left': [], 'right': []}
    previous_frame, previous_sign, move_origin = None, None, None
    def finish(side):
        rows = active[side]
        if len(rows) >= 2:
            # Max pairwise separation, not diagonal of a bounding box.
            world = max(math.dist(a['world'], b['world']) for a in rows for b in rows)
            view = max(math.dist(a['viewLogical'], b['viewLogical']) for a in rows for b in rows)
            segments.append({'side': side, 'firstSample': rows[0]['sample'], 'lastSample': rows[-1]['sample'],
                'sampleCount': len(rows), 'worldRangeUnits': world,
                'viewRangeLogicalPixelsAt1x': view, 'viewRangePixelsAt1_25x': view*1.25})
        active[side] = []
    for row in trace['rows']:
        distance += math.hypot(row['dxRaw'], row['dyRaw'])/256
        moving = row['dxRaw'] != 0 or row['dyRaw'] != 0
        sign = (row['commandX'] > 0) - (row['commandX'] < 0)
        eligible = (moving or row['paused']) and row['dodgeRemaining'] == 0 and not row['dodgePressed']
        if not eligible:
            for side in active: finish(side)
            move_origin = None
            previous_frame = None
            result.append({**row, 'distanceUnits': distance, 'frame': None,
                           'clipEvidence': 'not walking: idle/dodge excluded, no invented source frame'})
            continue
        if move_origin is None: move_origin = row['tick']
        frame = int(((row['tick']-move_origin)*32/60) if policy == 'fixed-time' else distance/120*16) % 16
        # Reversal is a separately marked unsupported facing, never a fictitious planted continuity.
        if (previous_frame is not None and frame < previous_frame) or (previous_sign is not None and sign != previous_sign):
            for side in active: finish(side)
        contacts = {}
        for leg in poses[frame]['legs']:
            side = leg['side']
            if leg['contact']:
                point = contact(row, leg)
                contacts[side] = point
                active[side].append({**point, 'sample': row['sample']})
            else: finish(side)
        result.append({**row, 'distanceUnits': distance, 'frame': frame, 'contacts': contacts,
            'clipEvidence': 'hypothetical exported south pose, not observed displayed frame'})
        previous_frame, previous_sign = frame, sign
    for side in active: finish(side)
    return {'scenario': trace['name'], 'policy': policy,
        'facingLimit': 'South source valid only for negative diagonal projected travel. Cardinal, sliding and reverse rows are deliberately held-south diagnostics, NOT authored facings.',
        'phaseLimit': 'Fixed-time anchored at first eligible moving tick, restarts after nonwalking. Distance uses accumulated actual travel/120. Neither asserts actual SpriteKit phase/restart selection.',
        'totalDistanceUnits': distance, 'segments': segments,
        'maxWorldRangeUnits': max((s['worldRangeUnits'] for s in segments), default=None),
        'maxViewRangeLogicalPixels': max((s['viewRangeLogicalPixelsAt1x'] for s in segments), default=None),
        'rows': result}

def main():
    traces = read('core-traces.json')['traces']
    baseline, revised = read('baseline-poses.json'), read('candidate-poses.json')
    results = []
    for trace in traces:
        for policy in ('fixed-time', 'distance-phase'):
            control = analyze(trace, baseline, policy)
            proposal = analyze(trace, revised, policy)
            if control != proposal:
                raise ValueError('Contact-preserving proposal unexpectedly changed ground contact')
            control['sourceVariants'] = ['unchanged-walk-control', 'bounded-brisk-recovery-proposal']
            results.append(control)
    packet = {'status': 'ACTUAL_CORE_PLUS_EXPORTED_SOURCE_MODEL_NOT_NATIVE_DISPLAY',
        'threshold': None, 'visualAcceptance': 'UNREVIEWED',
        'coordinateMethod': 'Q8 positions /256. Ground P(x,y)=((x-y)/sqrt2,(x+y)/(2sqrt2)). Source toe local view=(toe.x,-0.5*toe.y), source ground height=0. Inverse P recovers modeled ground world position. Native actual frame/transform still required.',
        'sourceHashes': {n: hashlib.sha256((HERE/n).read_bytes()).hexdigest() for n in ('core-traces.json','baseline-poses.json','candidate-poses.json')},
        'results': results}
    (HERE/'contact-comparison.json').write_text(json.dumps(packet, indent=2, allow_nan=False)+'\n')
    lines = ['# First authoritative trace findings', '', 'Actual Simulation.step positions joined to exported source contacts. Not observed display slip. No pass/fail slip threshold.', '', '| Case | Phase model | Travel units | Maximum contact span world | View logical px |', '|---|---|---:|---:|---:|']
    for result in results:
        def fmt(x): return 'not sampled' if x is None else f'{x:.6f}'
        lines.append(f"| {result['scenario']} | {result['policy']} | {result['totalDistanceUnits']:.6f} | {fmt(result['maxWorldRangeUnits'])} | {fmt(result['maxViewRangeLogicalPixels'])} |")
    lines += ['', 'Cardinal, slide and reversal use a deliberately held south source to expose the missing facing/contact problem, not to claim a correct facing. Idle/collision-stop and dodge do not receive fabricated walk contacts. Pause is the core no-step control only.', '', 'The source correction lowers recovery pelvis rise while retaining all foot coordinates, speed and cycle time. Therefore both source variants have identical modeled support slip. This is an honest motion-shape proposal, not a claimed slip fix. Partial-input policy remains unselected until native comparison.']
    (HERE/'first-findings.md').write_text('\n'.join(lines)+'\n')
    print('\n'.join(lines))

if __name__ == '__main__': main()
