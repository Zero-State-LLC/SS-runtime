#!/usr/bin/env python3
"""Verify a fresh focused xcresult export. Read-only, no synthetic result promotion.
Arguments: result-summary.json test-tree.json exported-attachments-directory
Obtain these with xcresulttool (see README). Does not certify visual quality.
"""
import hashlib
import io
from PIL import Image
import json
import math
import re
from pathlib import Path
import struct
import sys

TEST = 'ExistingArtViewportTests/testExistingArtViewportEvidence()'
EXPECTED = {f'viewport-{f}-{s}' for f in ('se', 'reference', 'inset')
            for s in ('standard', 'xl-reduced')} | {
                f'upgrade-{f}-{s}' for f in ('se', 'reference') for s in ('large', 'ax3')}


def need(ok, message):
    if not ok:
        raise ValueError(message)


def validate_result(summary, tree):
    need(summary.get('result') == 'Passed' and summary.get('totalTestCount') == 1
         and summary.get('passedTests') == 1 and summary.get('failedTests') == 0
         and summary.get('skippedTests') == 0 and summary.get('expectedFailures') == 0,
         'Need exactly one passing focused test with no skips or failures')
    cases = []
    def walk(node):
        if node.get('nodeType') == 'Test Case':
            cases.append(node)
        for child in node.get('children', []):
            walk(child)
    for node in tree['testNodes']:
        walk(node)
    need(len(cases) == 1 and cases[0].get('nodeIdentifier') == TEST
         and cases[0].get('result') == 'Passed', 'Wrong focused test identity')


def validate_packet(packet, plates):
    need(packet['schema'] == 'existing-art-viewports-001', 'Unknown schema')
    captures = packet['captures']
    need(len(captures) == 10 and {c['attachment'] for c in captures} == EXPECTED,
         'Missing, duplicate or unexpected capture')
    need(set(plates) == EXPECTED, 'Attachment census differs')
    resources = packet['resourceInventory']
    need(bool(resources) and len({r['assetID'] for r in resources}) == len(resources),
         'Empty or duplicate resource inventory')
    for resource in resources:
        need(len(resource['sha256']) == 64 and all(c in '0123456789abcdef' for c in resource['sha256'])
             and resource['bytes'] > 0, 'Malformed resource record')
    hosted_bounds = []
    for capture in captures:
        name = capture['attachment']
        data = plates[name]
        need(hashlib.sha256(data).hexdigest() == capture['sha256'], 'PNG hash mismatch')
        need(data[:8] == b'\x89PNG\r\n\x1a\n' and data[12:16] == b'IHDR', 'Invalid PNG header')
        with Image.open(io.BytesIO(data)) as image:
            image.load()
            decoded_dimensions = list(image.size)
        dimensions = list(struct.unpack('>II', data[16:24]))
        need(decoded_dimensions == dimensions, 'Decoded dimensions differ')
        expected = [667, 375] if '-se-' in name else [844, 390]
        need(dimensions == capture['pixels'] == capture['logicalSize'] == expected,
             'Wrong source-pixel or logical dimensions')
        if name.startswith('viewport-'):
            inset = name.startswith('viewport-inset-')
            need(capture['syntheticInsetsTLBR'] == ([0, 47, 8, 47] if inset else [0, 0, 0, 0]),
                 'Synthetic safe-area fixture changed')
            need(capture['safeSize'] == ([750, 382] if inset else expected), 'Safe size changed')
            reduced = name.endswith('xl-reduced')
            need(capture['hudScale'] == (1300 if reduced else 1000)
                 and capture['reducedMotion'] is reduced, 'Settings mislabelled')
            need(capture['hudChildCount'] > 0 and capture['kind'] == 'GameScene-offscreen-aspectFit',
                 'Missing real scene HUD evidence')
        else:
            need(capture['kind'] == 'hosted-production-UpgradeSelectionView'
                 and capture['dynamicType'] == ('accessibility3' if name.endswith('ax3') else 'large'),
                 'Hosted UI mislabelled')
            need(capture.get('requestedSize') == expected
                 and capture.get('logicalSizeRole') == 'requested-output-canvas-not-host',
                 'Requested output canvas must not be presented as actual host size')
            for field in ('hostViewBounds', 'windowBounds'):
                bounds = capture.get(field)
                need(isinstance(bounds, list) and len(bounds) == 4
                     and all(isinstance(value, (int, float)) and not isinstance(value, bool)
                             and math.isfinite(value) for value in bounds)
                     and bounds[2] > 0 and bounds[3] > 0, 'Missing/invalid actual UIKit bounds')
            need(capture.get('captureMapping') == 'drawHierarchy at host bounds into requested-size canvas, clipped if larger, no resize',
                 'Unknown hosted capture mapping')
            hosted_bounds.append({'attachment': name, 'requestedSize': expected,
                'hostViewBounds': capture['hostViewBounds'], 'windowBounds': capture['windowBounds'],
                'requestedViewportObserved': capture['hostViewBounds'] == [0, 0, *expected]
                    and capture['windowBounds'] == [0, 0, *expected]})
    need('physical-device operation' in packet['unsupported']
         and 'coherent-source acceptance' in packet['unsupported'], 'Missing scope limits')
    return {'status': 'TECHNICAL_EXPORT_VERIFIED_VISUAL_UNREVIEWED', 'captures': 10,
            'inventoryRecords': len(resources), 'physicalDevice': 'NOT_RUN',
            'hostedBounds': hosted_bounds,
            'resourceScope': packet['resourceScope']}


def verify(summary, tree, exports):
    validate_result(summary, tree)
    exports = Path(exports).resolve()
    plates, packets = {}, []
    for case in json.loads((exports / 'manifest.json').read_text()):
        need(case.get('testIdentifier') == TEST, 'Wrong attachment test identity')
        for item in case['attachments']:
            path = (exports / item['exportedFileName']).resolve()
            need(path.is_relative_to(exports) and path.is_file(), 'Export path escape or absent file')
            name = item['suggestedHumanReadableName']
            # xcresulttool appends occurrence index and attachment UUID.
            stem = re.sub(r'_\d+_[0-9A-Fa-f-]{36}(?=\.(?:png|json)$)', '', name)
            stem = stem.removesuffix('.png').removesuffix('.json')
            if stem in EXPECTED:
                need(stem not in plates, 'Duplicate plate')
                plates[stem] = path.read_bytes()
            elif stem == 'existing-art-viewports-records':
                packets.append(json.loads(path.read_text()))
    need(len(packets) == 1, 'Need exactly one evidence record')
    return validate_packet(packets[0], plates)


if __name__ == '__main__':
    try:
        result = verify(json.loads(Path(sys.argv[1]).read_text()),
                        json.loads(Path(sys.argv[2]).read_text()), sys.argv[3])
        print(json.dumps(result, indent=2))
    except (ValueError, KeyError, IndexError, OSError) as error:
        sys.exit(str(error))
