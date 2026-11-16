"""Fail-closed static encounter evidence reader. Does not run a simulator."""
import argparse
import hashlib
import json
from pathlib import Path
import re
from PIL import Image
import subprocess

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
TEST = 'ExistingArtEncounterTests/testLegalPilotExistingArtEncounterEvidence()'
WANTED = {f'camera-integrity-{n}' for n in range(4)} | {
    'cameraDestroyed', 'playerDamaged', 'entityDied', 'dense', 'hostile', 'mines', 'telegraphs', 'fieldOcclusion'}


def need(ok, message):
    if not ok:
        raise ValueError(message)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def load(path):
    return json.loads(Path(path).read_text())


def safe(root, name):
    root = Path(root).resolve()
    path = (root / name).resolve()
    need(path.is_relative_to(root) and path.is_file(), 'Path escape or missing file')
    return path


def expected_resources():
    contracts = ROOT / 'Sources/SurveillanceCore/Resources/contracts'
    presentation = load(contracts / 'presentation-assets-003.json')
    reachable = set()
    for key in ['requiredAssetIds', 'audioEventIds', 'musicAssetIds', 'environmentAssetIds']:
        reachable.update(presentation.get(key, []))
    for clip in load(contracts / 'clip-metadata-001.json')['clips']:
        reachable.update(clip['frameIds'])
    result = {}
    for entry in load(contracts / 'asset-catalog-001.json')['entries']:
        row = entry['record']
        if (entry['admissionDecision'] in {'plannedOriginal', 'adaptedAdmitted', 'originalAccepted'}
                and row['runtimeRequired'] and row['assetId'] in reachable
                and not (row.get('runtimePath') or '').startswith('ArtSources/')):
            need(row.get('runtimePath'), 'Reachable resource has no runtime path')
            result[row['assetId']] = row['runtimePath']
    need(result, 'No expected runtime inputs')
    return result


def validate_result(summary, tree):
    need(summary.get('result') == 'Passed' and summary.get('passedTests') == 1
         and summary.get('failedTests') == 0 and summary.get('skippedTests') == 0
         and summary.get('expectedFailures') == 0, 'Require one genuine passing native test')
    cases = []
    def walk(node):
        if node.get('nodeType') == 'Test Case':
            cases.append(node)
        for child in node.get('children', []):
            walk(child)
    for node in tree['testNodes']:
        walk(node)
    need(len(cases) == 1 and cases[0].get('nodeIdentifier') == TEST
         and cases[0].get('result') == 'Passed', 'Wrong native test identity')


def attachments(exports):
    exports = Path(exports).resolve()
    found = {}
    for case in load(exports / 'manifest.json'):
        for item in case['attachments']:
            name = item.get('suggestedHumanReadableName', '')
            match = re.match(r'(existing-art-(?:tick-\d+|encounter-records|legal-commands))(?:[_.]|$)', name)
            if not match:
                continue
            key = match.group(1)
            need(not item.get('isAssociatedWithFailure', False), 'Failure-associated attachment')
            need(key not in found, 'Duplicate attachment')
            found[key] = safe(exports, item['exportedFileName'])
    need('existing-art-encounter-records' in found and 'existing-art-legal-commands' in found,
         'Missing evidence records or legal commands')
    return found


def validate_packet(packet, files, expected=None, asset_root=None):
    need(packet['schema'] == 'existing-art-encounters-v1', 'Wrong schema')
    need(packet['scenarioSeeded'] is False and packet['seed'] == 1, 'Seeded or wrong legal route')
    need(packet['driver'] == 'DebugAutopilot run / ghostStep / seed1', 'Wrong driver')
    need(0 < packet['terminalTick'] <= packet['tickLimit'] == 6000, 'Tick bounds')
    need(packet['finalDigest'] == packet['replayDigest'], 'Final replay digest differs')
    need(packet['sourceFidelity'] == 'BLOCKED' and packet['ownerAcceptance'] == 'NOT_GRANTED'
         and packet['productionAdmission'] == 'NOT_GRANTED', 'Acceptance boundary changed')
    need(packet['evidenceKind'] == 'static paused GameScene existing production art and projection', 'Scope changed')
    contracts = ROOT / 'Sources/SurveillanceCore/Resources/contracts'
    contract_names = {'asset-catalog-001.json', 'presentation-assets-003.json', 'clip-metadata-001.json'}
    need(set(packet['contractSHA256']) == contract_names, 'Contract census differs')
    for name in contract_names:
        need(packet['contractSHA256'][name] == sha((contracts / name).read_bytes()), 'Contract bytes differ')
    expected = expected_resources() if expected is None else expected
    asset_root = ROOT / 'Sources/SurveillanceCore/Resources/RuntimeAssets' if asset_root is None else asset_root
    inventory = packet['runtimeInputs']
    need(len(inventory) == len(expected) and {r['assetId'] for r in inventory} == set(expected), 'Resource census differs')
    for row in inventory:
        need(row['path'] == expected[row['assetId']], 'Resource path differs')
        data = safe(asset_root, row['path']).read_bytes()
        need(sha(data) == row['sha256'] and len(data) == row['bytes'], 'Resource bytes differ')
    commands = files['existing-art-legal-commands'].read_bytes()
    need(sha(commands) == packet['replaySHA256'], 'Command attachment differs')
    replay = json.loads(commands)
    need(replay['seed'] == 1 and replay['ticks'] == packet['terminalTick']
         and replay['digest'] == packet['finalDigest'], 'Command replay identity differs')
    rows = packet['captures']
    need(1 < len(rows) <= len(WANTED), 'Empty or unbounded capture count')
    names, ticks, tags = set(), [], set()
    for row in rows:
        need(row['image'] == f"existing-art-tick-{row['tick']}", 'Image tick mismatch')
        need(row['image'] not in names, 'Duplicate capture')
        names.add(row['image'])
        ticks.append(row['tick'])
        need(row['digest'] == row['captureDigestAfter'], 'Capture changed simulation')
        fresh = set(row['tags'])
        need(fresh and fresh <= WANTED and not fresh.intersection(tags), 'Duplicate or invalid coverage tags')
        tags.update(fresh)
        data = files[row['image']].read_bytes()
        need(sha(data) == row['pngSHA256'], 'Image attachment differs')
        with Image.open(files[row['image']]) as image:
            need(image.format == 'PNG' and image.size == (row['width'], row['height']), 'Image dimensions or format differ')
            image.verify()
        need(row['width'] > 0 and row['height'] > 0, 'Empty image')
        for camera in row['cameras']:
            need(0 <= camera['integrity'] <= 3, 'Invalid Camera integrity')
            if not camera['fieldVisible']:
                need(camera['fieldNodePresent'] is False, 'Field remains rendered after field-off')
        for tag in fresh:
            if tag.startswith('camera-integrity-'):
                need(any(c['integrity'] == int(tag[-1]) for c in row['cameras']), 'Unobserved Camera state claimed')
            elif tag in {'cameraDestroyed', 'playerDamaged', 'entityDied'}:
                need(any(e['type'] == tag and e['tick'] == row['tick'] for e in row['events']), 'Event not present at capture')
            elif tag == 'dense':
                need(row['nearbyEnemyCount'] >= 2 and row['projectileCount'] > 0, 'Not the established encounter')
            elif tag in {'hostile', 'mines', 'telegraphs'}:
                key = {'hostile': 'hostileProjectileCount', 'mines': 'mineCount', 'telegraphs': 'telegraphCount'}[tag]
                need(row[key] > 0, 'Missing claimed combat state')
            elif tag == 'fieldOcclusion':
                probe = row['fieldOcclusion']
                need(probe['clearContains'] is True and probe['clippedContains'] is False, 'No field occlusion probe')
    need(ticks == sorted(set(ticks)) and ticks[-1] <= packet['terminalTick'], 'Capture ticks out of order')
    need(tags == set(packet['observed']) and 'dense' in tags, 'Coverage census differs')
    need(set(packet['notObserved']) == WANTED - tags, 'Absent coverage not disclosed')
    need(set(files) == names | {'existing-art-encounter-records', 'existing-art-legal-commands'}, 'Attachment census differs')
    return {'status': 'STATIC_EXISTING_ART_NOT_ACCEPTANCE', 'captures': len(rows),
            'resources': len(inventory), 'observed': sorted(tags), 'notObserved': sorted(WANTED - tags)}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('exports', type=Path)
    parser.add_argument('xcresult', type=Path)
    args = parser.parse_args()
    def query(kind):
        return json.loads(subprocess.check_output(['xcrun', 'xcresulttool', 'get', 'test-results',
                                                  kind, '--path', str(args.xcresult)]))
    validate_result(query('summary'), query('tests'))
    files = attachments(args.exports)
    result = validate_packet(load(files['existing-art-encounter-records']), files)
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
