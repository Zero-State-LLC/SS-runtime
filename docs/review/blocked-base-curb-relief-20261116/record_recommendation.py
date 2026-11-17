"""Serialize the coordinator's already-written, exact final source decision.
No source editing, art generation or native execution. Refuses overwrite.
"""
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
SOURCE = HERE / 'source/attempt-02'
EXPECTED = '5b0943d029eadaf00d4e2d039dbeeda3e3353241c7881f28dd370c3295ab1891'


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def dep(path):
    return dict(path=str(path.relative_to(ROOT)), sha256=digest(path))


if __name__ == '__main__':
    manifest = SOURCE / 'manifest.json'
    review = HERE / 'SOURCE-REVIEW-FINAL.md'
    if digest(manifest) != EXPECTED:
        raise SystemExit('Final source changed. New coordinator decision required.')
    source = json.loads(manifest.read_text())
    dependencies = []
    for name, expected in sorted(source['files'].items()):
        path = SOURCE / name
        if path.resolve().parent != SOURCE.resolve() and SOURCE.resolve() not in path.resolve().parents:
            raise SystemExit('Source path escape')
        if digest(path) != expected:
            raise SystemExit('Source dependency changed: ' + name)
        dependencies.append(dep(path))
    envelope = dict(schema='blocked-base-curb-recommendations-009',
                    manifest=dep(manifest), dependencies=dependencies,
                    recommendation=dict(reviewerRole='coordinator', decision='recommended',
                                        scope='isolated-ordinary-scene', manifestSHA256=EXPECTED,
                                        evidence=dep(review)))
    with (HERE / 'recommendations.json').open('x') as handle:
        json.dump(envelope, handle, indent=2)
        handle.write('\n')
    print('Serialized existing final coordinator decision:', EXPECTED)
