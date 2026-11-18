#!/usr/bin/env python3
"""Pixel/registration symptom probe. Not an aesthetic acceptance classifier."""
import argparse
import json
from pathlib import Path
from PIL import Image, ImageChops, ImageFilter

ROOT = Path(__file__).resolve().parents[3]
OLD = ROOT / 'docs/review/scene-source-assembly-20261116'


def actor_image(actor, source, row, image_size):
    density = image_size[0] / 704
    scale = density * row['zoom']
    width, height = [round(v * scale) for v in actor['size']]
    x = image_size[0] / 2 + (actor['projectedRoot'][0] - row['centerWorld'][0]) * density
    y = image_size[1] / 2 - (actor['projectedRoot'][1] - row['centerWorld'][1]) * density
    left = round(x - actor['anchor'][0] * width)
    top = round(y - (1 - actor['anchor'][1]) * height)
    with Image.open(source) as src:
        sprite = src.convert('RGBA').resize((width, height), Image.Resampling.BILINEAR)
    canvas = Image.new('RGBA', image_size)
    canvas.paste(sprite, (left, top))
    return canvas


def actor_mask(actor, source, row, image_size):
    return actor_image(actor, source, row, image_size).getchannel('A')


def probe(capture, prepared):
    record = json.loads((capture / 'source-scene-records.json').read_text())
    results = []
    for row in record['captures']:
        if row['arm'] != 'candidate':
            continue
        actors = {a['name']: a for a in row['actors']}
        camera = actors['sprite-camera-3']
        stone = actors['benchmark-building']
        player = actors['sprite-player']
        with Image.open(capture / (row['name'] + '-native.png')) as src:
            image = src.convert('RGB')
        cm = actor_mask(camera, prepared / 'camera.png', row, image.size)
        expected_camera = actor_image(camera, prepared / 'camera.png', row, image.size).convert('RGB')
        core = cm.filter(ImageFilter.MinFilter(3))
        diff = ImageChops.difference(image, expected_camera).tobytes()
        camera_deltas = [(r + g + b) / 3 for r, g, b, alpha in zip(diff[0::3], diff[1::3], diff[2::3], core.tobytes()) if alpha > 240]
        camera_match = sum(delta < 25 for delta in camera_deltas) / max(1, len(camera_deltas))
        sm = actor_mask(stone, prepared / 'stone.png', row, image.size)
        pm = actor_mask(player, prepared / 'player.png', row, image.size)
        overlap = ImageChops.multiply(cm, sm) if stone['actualZ'] > camera['actualZ'] else Image.new('L', image.size)
        mass = sum(cm.tobytes())
        covered = sum(overlap.tobytes()) / max(1, mass)
        # White-blue pixels in the narrow exterior band of the exact registered source.
        # This tests the unwanted outline in captured pixels, not texture metadata.
        radius = 2 * round(image.width / 704 * row['zoom']) + 1
        ring = ImageChops.subtract(pm.filter(ImageFilter.MaxFilter(radius)), pm)
        raw = image.tobytes()
        samples = [(r, g, b) for r, g, b, alpha in zip(raw[0::3], raw[1::3], raw[2::3], ring.tobytes()) if alpha > 100]
        pale = sum(r > 190 and g > 205 and b > 210 and b >= r for r, g, b in samples)
        halo_ratio = pale / max(1, len(samples))
        results.append({'zoom': row['zoom'], 'cameraCoveredByStoneFraction': covered,
                        'playerExteriorPalePixels': pale, 'playerExteriorSamples': len(samples),
                        'playerExteriorPaleRatio': halo_ratio,
                        'cameraCapturedPixelMatchRatio': camera_match, 'cameraCoreSamples': len(camera_deltas),
                        'cameraReadable': covered < .2 and camera_match > .70, 'playerNoPaleHalo': halo_ratio < .02})
    if len(results) != 3:
        raise ValueError('Expected three real candidate zooms')
    return {'kind': 'REGISTERED_SILHOUETTE_AND_CAPTURED_PIXEL_QA_NOT_ACCEPTANCE',
            'passed': all(r['cameraReadable'] and r['playerNoPaleHalo'] for r in results), 'results': results}


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--capture', type=Path, default=OLD / 'native-capture-1040')
    parser.add_argument('--prepared', type=Path, default=OLD / 'native-inputs-v4')
    args = parser.parse_args()
    report = probe(args.capture, args.prepared)
    print(json.dumps(report, indent=2))
    raise SystemExit(0 if report['passed'] else 1)
