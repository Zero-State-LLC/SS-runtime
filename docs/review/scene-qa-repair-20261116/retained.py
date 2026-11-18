#!/usr/bin/env python3
"""Verify retained native scene evidence without Xcode or a new native-run claim."""
import argparse
import json
from pathlib import Path
from PIL import Image
import importlib.util

_spec = importlib.util.spec_from_file_location('_scene_qa_v5_native_retained', Path(__file__).resolve().with_name('native.py'))
n = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(n)


def verify(capture, prepared=None):
    capture = Path(capture)
    prepared = Path(prepared) if prepared else n.HERE / 'native-inputs-v5'
    report = n.load(capture / 'verification.json')
    n.a.need(report['status'] == n.STATUS, 'Wrong retained evidence status')
    n.a.need(report['fixtureVersion'] == n.FIXTURE_VERSION, 'Historical fixture is not current evidence')
    n.a.need(report['nativeTests'] == 1 and report['captures'] == 6 and report['images'] == 18,
             'Wrong retained capture census')
    for key in ('ownerAcceptance', 'physicalDeviceEvidence', 'animationFamilyEvidence'):
        n.a.need(report[key] is False, 'Unearned retained evidence claim')
    files = report['files']
    n.a.need(isinstance(files, dict) and len(files) == 22, 'Wrong retained file census')
    n.a.need(set(files) == {name + '.png' for name in n.NAMES} | {'source-scene-records.json', 'attachment-manifest.json', 'summary.json', 'tests.json'}, 'Wrong exact retained file names')
    n.a.need({p.name for p in capture.iterdir()} == set(files) | {'verification.json'},
             'Missing or unexpected retained file')
    for name, digest in files.items():
        n.a.need(Path(name).name == name and name not in ('.', '..'), 'Retained path escape')
        path = capture / name
        n.a.need(path.is_file() and not path.is_symlink(), 'Retained file is missing or symlinked')
        n.a.need(n.sha(path) == digest, 'Retained file hash drift: ' + name)
    input_path = prepared / 'native-inputs.json'
    n.a.need(input_path.is_file() and not input_path.is_symlink(), 'Missing/symlinked retained preparation')
    inputs = n.load(input_path)
    n.a.need(inputs == n.expected_input(), 'Retained preparation is not current exact binding')
    n.a.need(n.sha(input_path) == report['inputSHA256'], 'Retained input manifest drift')
    for source in inputs['sources']:
        path = n.a.safe(prepared, source['file'])
        n.a.need(n.sha(path) == source['sha256'], 'Retained prepared PNG drift')
    n.validate_result(n.load(capture / 'summary.json'), n.load(capture / 'tests.json'))
    record = n.load(capture / 'source-scene-records.json')
    captures = n.validate_records(record, inputs, n.sha(input_path))
    for name, digest in record['controlSHA256'].items():
        n.a.need(n.sha(n.ROOT / 'AppTests/BenchmarkAssets' / name) == digest, 'Retained original control drift')
    n.a.need(len(record.get('runtimeSHA256', {})) == 2, 'Retained runtime ground census drift')
    for name, digest in record['runtimeSHA256'].items():
        n.a.safe(n.ROOT, name)
        matches = list((n.ROOT / 'Sources/SurveillanceCore/Resources/RuntimeAssets').rglob(Path(name).name))
        n.a.need(len(matches) == 1 and n.sha(matches[0]) == digest, 'Retained runtime ground drift')
    n.a.need(record['harnessSourceReadSHA256'] == report['harnessSourceReadSHA256'], 'Source-read provenance disagreement')
    executable = report['testExecutable']
    n.a.need(executable['loadedSHA256'] == executable['expectedBuildSHA256'] == record['loadedTestExecutable']['sha256'],
             'Imported executable provenance disagreement')
    n.a.need(executable['loadedPath'] == record['loadedTestExecutable']['path'], 'Loaded executable path disagreement')
    built = Path(executable['expectedBuildPath'])
    n.a.need(built.is_absolute() and built.name == 'SSRuntimeTests' and built.parent.name == 'SSRuntimeTests.xctest', 'Invalid preserved build executable path')
    expected_pngs = set()
    for row in captures:
        width, height = row['nativePixels']
        n.a.need(width % 704 == 0 and height % 326 == 0 and width // 704 == height // 326 and 1 <= width // 704 <= 4,
                 'Wrong retained pixel scale')
        for suffix, digest in row['pngSHA256'].items():
            name = row['name'] + suffix + '.png'
            expected_pngs.add(name)
            n.a.need(files.get(name) == digest, 'Capture/image hash disagreement')
            with Image.open(capture / name) as image:
                size = (width // 2, height // 2) if suffix == '-half' else (width, height)
                n.a.need(image.format == 'PNG' and image.size == size, 'Wrong retained PNG dimensions')
                image.verify()
    n.a.need(expected_pngs == {name for name in files if name.endswith('.png')}, 'Retained PNG census drift')
    return {'status': 'RETAINED_BYTES_AND_CONTRACT_VERIFIED_NOT_NEW_NATIVE_RUN',
            'fixtureVersion': n.FIXTURE_VERSION, 'captures': 6, 'images': len(expected_pngs),
            'ownerAcceptance': False, 'physicalDeviceEvidence': False,
            'binaryCheck': 'agreement of preserved original import records, not a fresh local binary comparison'}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('capture', type=Path)
    parser.add_argument('--prepared', type=Path)
    args = parser.parse_args()
    print(json.dumps(verify(args.capture, args.prepared), indent=2))
