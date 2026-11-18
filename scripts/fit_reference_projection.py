#!/usr/bin/env python3
"""BP-001 direction-only ground fit, never a recovered camera calibration."""
import argparse
import hashlib
import json
import math
import random
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT = ROOT / 'docs/review/bp001-reference-trial-20261116/landmarks.json'


def angle(segment):
    dx = segment['end'][0] - segment['start'][0]
    dy = segment['end'][1] - segment['start'][1]
    if not math.isfinite(dx + dy) or dx <= 0 or dy == 0:
        raise ValueError('Expected finite, rightward, nonhorizontal segment')
    return math.atan2(dy, dx)


def fit(segments):
    means = {}
    for axis in ('east', 'north'):
        values = [angle(s) for s in segments if s['use'] == 'fit' and s['axis'] == axis]
        if len(values) < 2:
            raise ValueError('Need at least two independently labeled fit segments per axis')
        means[axis] = sum(values) / len(values)
    shallow, steep = math.tan(means['east']), -math.tan(means['north'])
    if shallow <= 0 or steep <= 0:
        raise ValueError('Expected east down-right and north up-right in image coordinates')
    scale = math.sqrt(shallow * steep)
    rotation = -math.atan(math.sqrt(shallow / steep))
    return rotation, scale, means


def project(x, y, rotation, scale):
    c, s = math.cos(rotation), math.sin(rotation)
    return c*x - s*y, scale*(s*x + c*y)


def inverse(x, y, rotation, scale):
    c, s = math.cos(rotation), math.sin(rotation)
    return c*x + s*y/scale, -s*x + c*y/scale


def report(path):
    raw = path.read_bytes()
    data = json.loads(raw)
    reference = (path.parent / data['reference']).resolve()
    rotation, scale, means = fit(data['segments'])
    residuals = []
    for segment in data['segments']:
        observed = angle(segment)
        predicted = means[segment['axis']]
        residuals.append(dict(id=segment['id'], use=segment['use'],
                              observedImageAngleDegrees=math.degrees(observed),
                              fittedImageAngleDegrees=math.degrees(predicted),
                              residualDegrees=math.degrees(observed-predicted)))
    rng = random.Random(110016)
    rotations, scales = [], []
    uncertainty = data['endpointUncertaintyPixels']
    for _ in range(4096):
        perturbed = []
        for segment in data['segments']:
            row = dict(segment)
            for point in ('start', 'end'):
                row[point] = [v + rng.uniform(-uncertainty, uncertainty) for v in segment[point]]
            perturbed.append(row)
        r, k, _ = fit(perturbed)
        rotations.append(math.degrees(r))
        scales.append(k)
    vectors = []
    checks = 0
    for name, x, y in [('E',1,0),('NE',1,1),('N',0,1),('NW',-1,1),
                       ('W',-1,0),('SW',-1,-1),('S',0,-1),('SE',1,-1)]:
        length = math.hypot(x, y)
        unit = x/length, y/length
        p = project(*unit, rotation, scale)
        vectors.append(dict(worldDirection=name, sceneVector=list(p), screenVector=[p[0],-p[1]]))
        for magnitude in (0.25,0.5,1,120):
            a = unit[0]*magnitude, unit[1]*magnitude
            recovered = inverse(*project(*a,rotation,scale),rotation,scale)
            assert max(abs(a[i]-recovered[i]) for i in (0,1)) < 1e-10
            checks += 1
    c, s = math.cos(rotation), math.sin(rotation)
    return dict(status='DIRECTION_FIT_NOT_CAMERA_OR_ART_ACCEPTANCE',
                referenceSHA256=hashlib.sha256(reference.read_bytes()).hexdigest(),
                landmarksSHA256=hashlib.sha256(raw).hexdigest(),
                sceneRotationDegrees=math.degrees(rotation), groundYScale=scale,
                sceneMatrix=[[c,-s],[scale*s,scale*c]], determinant=scale,
                normalizedViewportWorldArea=704*326/scale,
                residuals=residuals, directions=vectors, offlineRoundTrips=checks,
                sensitivity=dict(method='4096 seeded uniform endpoint perturbations within +/-8px; sampled range, NOT statistical confidence or exhaustive bound',
                                 rotationDegrees=[min(rotations),max(rotations)],
                                 yScale=[min(scales),max(scales)]),
                conventions=['ground x scale is fixed to1, not recovered world scale',
                             'scene translation and world-axis association are trial choices',
                             'upright source art is unchanged, not fitted to this view'],
                limitations=data['limitations'])


def diagram(data):
    # SVG review diagram references the original image without changing its bytes.
    parts = ['<svg xmlns="http://www.w3.org/2000/svg" width="1672" height="941" viewBox="0 0 1672 941">',
             '<image href="../bp001-decision-20261116/street-corner-approved-concept.png" width="1672" height="941"/>']
    for i, segment in enumerate(data['segments'], 1):
        (x1,y1),(x2,y2) = segment['start'],segment['end']
        color = '#00ffff' if segment['use'] == 'fit' else '#ff66ff'
        parts.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{color}" stroke-width="3"/>')
        for x,y in (segment['start'],segment['end']):
            parts.append(f'<circle cx="{x}" cy="{y}" r="8" fill="none" stroke="{color}" stroke-width="2"/>')
        parts.append(f'<text x="{(x1+x2)/2}" y="{(y1+y2)/2}" fill="{color}" stroke="#000" stroke-width="0.5" font-family="sans-serif" font-size="24">{i}</text>')
    return '\n'.join(parts + ['</svg>']) + '\n'


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--landmarks',type=Path,default=DEFAULT)
    parser.add_argument('--check',action='store_true')
    args = parser.parse_args()
    result = report(args.landmarks)
    destination = args.landmarks.parent / 'ground-fit.json'
    svg = args.landmarks.parent / 'landmarks.svg'
    serialized = json.dumps(result,indent=2) + '\n'
    image = diagram(json.loads(args.landmarks.read_text()))
    if args.check:
        assert destination.read_text() == serialized, 'ground-fit.json drift'
        assert svg.read_text() == image, 'landmark diagram drift'
    else:
        destination.write_text(serialized)
        svg.write_text(image)
    print(json.dumps({k:result[k] for k in ('sceneRotationDegrees','groundYScale','residuals','sensitivity','offlineRoundTrips')},indent=2))


if __name__ == '__main__':
    main()
