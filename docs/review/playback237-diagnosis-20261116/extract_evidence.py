"""Re-extract the exact failed test attachments with hashes and payload identities."""
import hashlib
import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parent
SUMMARY = '0~0IRy-N5ahkoXp9wBprKuxVuk-zU2afvRdu8yGaGfTJ0annSBZOtzHFB8DTM8gXhlnuoXFJVRo1V8-SeZC41rwQ=='


def extract(bundle):
    raw = subprocess.check_output([
        'xcrun', 'xcresulttool', 'get', 'object', '--legacy', '--path', str(bundle),
        '--id', SUMMARY, '--format', 'json'])
    summary = json.loads(raw)
    attachments = []
    for activity in summary['activitySummaries']['_values']:
        for attachment in activity.get('attachments', {}).get('_values', []):
            index = len(attachments)
            name = attachment['name']['_value']
            if not name.endswith('-records'):
                raise ValueError('unexpected attachment')
            payload = attachment['payloadRef']['id']['_value']
            destination = ROOT / 'evidence' / f'act{index}.json'
            subprocess.run(['xcrun', 'xcresulttool', 'export', '--legacy',
                            '--path', str(bundle), '--id', payload,
                            '--output-path', str(destination), '--type', 'file'], check=True)
            attachments.append(dict(file=destination.name, name=name, payloadRef=payload,
                                    sha256=hashlib.sha256(destination.read_bytes()).hexdigest()))
    if len(attachments) != 6:
        raise ValueError('expected exactly six retained cases')
    manifest = dict(run=43803119616, artifact=14198828420, job=133087698819,
                    head='9769d922cc8f3e908c0d611dd2f48df6418089cd', summaryRef=SUMMARY, attachments=attachments)
    (ROOT / 'evidence' / 'attachments.json').write_text(json.dumps(manifest, indent=2) + '\n')


if __name__ == '__main__':
    extract(Path(sys.argv[1]))
