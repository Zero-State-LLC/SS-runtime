#!/usr/bin/env python3
"""Verify retained actual XCUI evidence, not physical accessibility or game resume."""
import hashlib
import json
from pathlib import Path
from PIL import Image, ImageOps

HERE = Path(__file__).resolve().parent
CASES = {
    'UpgradeInteractionTests/testDefaultTouchSelectsFirst()': ('default-large', 'signalJammer', 0),
    'UpgradeInteractionTests/testAccessibility3ScrollsToLastAndSelects()': ('--accessibility3', 'ghostStep', 2),
    'UpgradeInteractionTests/testAccessibility5ScrollsToLastAndSelects()': ('--accessibility5', 'ghostStep', 2),
}

def need(condition, message):
    if not condition:
        raise ValueError(message)

def load(path):
    return json.loads(Path(path).read_text())

def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()

def validate_result(summary, tree):
    need(summary['result'] == 'Passed', 'Result not passed')
    for key, expected in [('totalTestCount', 3), ('passedTests', 3), ('failedTests', 0), ('skippedTests', 0), ('expectedFailures', 0)]:
        need(summary[key] == expected, 'Incorrect result count: ' + key)
    cases = []
    def walk(nodes):
        for node in nodes:
            if node.get('nodeType') == 'Test Case':
                cases.append((node['nodeIdentifier'], node['result']))
            walk(node.get('children', []))
    walk(tree['testNodes'])
    need(len(cases) == 3 and set(cases) == {(name, 'Passed') for name in CASES}, 'Test identity mismatch')

def validate_record(record, case):
    argument, target, index = CASES[case]
    need(record['status'] == 'ACTUAL_XCUI_INTERACTION_ISOLATED_PRODUCTION_VIEW_NOT_FULL_GAME', 'Scope mismatch')
    need(record['dynamicTypeArgument'] == argument and record['target'] == target and record['selectionIndex'] == index, 'Selection identity mismatch')
    need(record['selectionResult'] == f'selected={index};count=1', 'Selection not exactly once')
    need(record['captureMethod'] == 'XCUIScreen.main.screenshot', 'Rejected window capture method')
    need(record['deviceOrientation'] == 'landscapeLeft', 'Orientation mismatch')
    need([record['windowWidth'], record['windowHeight']] == [667, 375], 'Window dimensions mismatch')
    need(type(record['swipes']) is int and 0 <= record['swipes'] <= 40, 'Swipe count invalid')
    if index == 2:
        need(record['swipes'] > 0 and record['initiallyHittable'] is False, 'Scroll was not required')
    need(len(record['accessibilityLabel']) > 40, 'Missing accessible description')
    for key in ('voiceOverSession', 'physicalDevice', 'gameResumeVerified'):
        need(record[key] is False, 'Unsupported claim: ' + key)

def verify(capture=HERE / 'capture'):
    capture = Path(capture).resolve()
    validate_result(load(capture / 'summary.json'), load(capture / 'tests.json'))
    manifest = load(capture / 'manifest.json')
    need(len(manifest) == 3 and {case['testIdentifier'] for case in manifest} == set(CASES), 'Attachment case census')
    inventory = load(capture / 'inventory.json')
    need(set(inventory) == {item['exportedFileName'] for case in manifest for item in case['attachments']} | {'summary.json', 'tests.json', 'manifest.json'}, 'Inventory census mismatch')
    for name, digest in inventory.items():
        path = (capture / name).resolve()
        need(path.is_relative_to(capture), 'Inventory escape')
        need(sha(path) == digest, 'Retained file hash mismatch: ' + name)
    rows = []
    for case in manifest:
        need(len(case['attachments']) == 4, 'Expected three screenshots and one record')
        images, records = {}, []
        for item in case['attachments']:
            path = (capture / item['exportedFileName']).resolve()
            need(path.is_relative_to(capture) and path.is_file(), 'Attachment escape or missing')
            need(item['isAssociatedWithFailure'] is False, 'Failure attachment')
            name = item['suggestedHumanReadableName'].split('_')[0]
            if path.suffix == '.json':
                records.append(load(path))
            else:
                stage = name.rsplit('-', 1)[-1]
                need(stage in ('before', 'reachable', 'selected') and stage not in images, 'Screenshot stage mismatch')
                with Image.open(path) as raw:
                    image = ImageOps.exif_transpose(raw)
                    need(image.size == (1334, 750), 'Oriented screenshot dimensions mismatch')
                    need(image.convert('RGB').getcolors(maxcolors=64) is None, 'Blank screenshot')
                    image.close()
                images[stage] = path.name
        need(len(records) == 1 and set(images) == {'before', 'reachable', 'selected'}, 'Attachment census mismatch')
        validate_record(records[0], case['testIdentifier'])
        rows.append({'case': case['testIdentifier'], 'record': records[0], 'images': images})
    return rows

if __name__ == '__main__':
    rows = verify()
    print(json.dumps({'status': 'VERIFIED_ISOLATED_INTERACTION_NOT_FULL_GAME', 'tests': len(rows), 'screenshots': sum(len(row['images']) for row in rows), 'physicalDevice': False, 'voiceOverSession': False}, indent=2))
