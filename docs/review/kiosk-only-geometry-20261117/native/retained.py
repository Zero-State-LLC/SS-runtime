#!/usr/bin/env python3
"""Recheck retained native kiosk attachments without executing a simulator."""
import argparse
import json
from pathlib import Path
import native as n


def check(directory, executable):
    n.need(directory.is_dir() and directory.resolve() == directory.absolute(), 'Missing or aliased native output')
    receipt = directory / 'verification.json'
    n.need(receipt.is_file() and not receipt.is_symlink(), 'Missing or aliased native receipt')
    report = n.load(receipt)
    expected = report.get('files', {})
    n.need(set(p.name for p in directory.iterdir()) == set(expected) | {'verification.json'}, 'Native output inventory drift')
    for name, digest in expected.items():
        n.need(Path(name).name == name, 'Native output path escape')
        path = directory / name
        n.need(path.is_file() and not path.is_symlink() and n.sha(path) == digest, 'Native output hash drift: ' + name)
    prepared = n.expected_input()
    n.validate_prepared(prepared, n.HERE / 'prepared')
    input_sha = n.sha(n.HERE / 'prepared/native-inputs.json')
    n.need(report.get('status') == n.STATUS and report.get('fixtureVersion') == n.FIXTURE_VERSION, 'Wrong retained evidence identity')
    n.need(report.get('inputSHA256') == input_sha and report.get('nativeTests') == 1 and report.get('captures') == 6 and report.get('images') == 18, 'Wrong retained evidence census')
    n.need(report.get('ownerAcceptance') is False and report.get('physicalDeviceEvidence') is False, 'Invalid acceptance/device claim')
    n.validate_result(n.load(directory / 'summary.json'), n.load(directory / 'tests.json'))
    n.validate_attachment_manifest(n.load(directory / 'attachment-manifest.json'))
    record = n.load(directory / 'source-scene-records.json')
    rows = n.validate_records(record, prepared, input_sha)
    actual_executable = n.v9.validate_executable(record, executable)
    n.need(report.get('testExecutable') == actual_executable, 'Retained executable receipt drift')
    n.verify_images({p.stem: p for p in directory.glob('*.png')}, rows)
    return dict(status=n.STATUS, captures=6, images=18, unchangedOutsideKioskCanvasPairs=3,
                inputSHA256=input_sha, testExecutable=actual_executable,
                ownerAcceptance=False, physicalDeviceEvidence=False)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('directory', type=Path)
    parser.add_argument('--test-executable', type=Path, required=True)
    args = parser.parse_args()
    print(json.dumps(check(args.directory, args.test_executable), indent=2))
