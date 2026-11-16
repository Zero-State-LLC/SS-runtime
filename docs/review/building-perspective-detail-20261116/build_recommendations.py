#!/usr/bin/env python3
"""Map coordinator-reviewed exact bytes into five v7 source recommendations.

This script does not review art or choose a source. Four explicit coordinator
approval hashes are mandatory. A stale manifest/review, missing geometry witness,
unexecuted final roof correction or changed dependency fails before any output.
Never launches native tools and never edits sources or the frozen Swift fixture.
"""
import argparse
import importlib.util
import json
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location('_building_review_mapping_v7', HERE / 'scene/native.py')
n = importlib.util.module_from_spec(spec)
spec.loader.exec_module(n)
FIELDS = ('canvasPixels', 'rootPixelsTopLeft', 'worldPosition', 'drawSizeWorld')
FROZEN_SWIFT = '92cf6adf3ebee3ddd970cda799b19fcffee190c1b5fd998f02f176f4dd403e01'


def ref(path, expected=None):
    relative = str(path.relative_to(n.ROOT))
    result = dict(path=relative, sha256=n.sha(path))
    n.dependency(result, n.ROOT)
    n.a.need(expected is None or result['sha256'] == expected, 'Source manifest byte drift: ' + relative)
    return result


def source_files(base, manifest, kiosk):
    """Bind ALL declared source/output/implementation bytes, plus source scripts.
    The final context repair explicitly reads retained attempt-01 geometry too.
    """
    paths = {}
    sections = [('inputs', base), ('outputs', base / 'output')] if kiosk else [('files', base), ('implementationSHA256', base)]
    for section, folder in sections:
        n.a.need(isinstance(manifest.get(section), dict) and bool(manifest[section]), 'Missing source manifest section: ' + section)
        for name, digest in manifest[section].items():
            path = n.a.safe(folder, name)
            record = ref(path, digest)
            n.a.need(record['path'] not in paths or paths[record['path']] == record, 'Conflicting dependency hashes')
            paths[record['path']] = record
    # Also bind auditing/source utility scripts that the author does not list as
    # render inputs. No attempt logs, Python caches or output mutation is involved.
    for path in sorted(base.glob('*.py')):
        paths[str(path.relative_to(n.ROOT))] = ref(path)
    if not kiosk:
        required = {'author.py', 'replay.py', 'test_context.py', 'repair_roof_density.py'}
        n.a.need(required <= set(manifest['implementationSHA256']), 'Final repair renderer must be manifest-bound')
        previous = base / 'attempt-01/geometry.json'
        paths[str(previous.relative_to(n.ROOT))] = ref(previous)
        geometry = n.load(base / 'geometry.json')
        n.a.need(geometry.get('roofTileWorldUnits') == 128, 'Final bounded roof-density repair has not been executed')
        n.a.need(manifest.get('status') == 'FINAL_BOUNDED_SOURCE_REVIEW_ONLY', 'Context final render manifest not available')
    return paths


def approval(base, review_sha, manifest_sha, kiosk):
    review = base / 'COORDINATOR-REVIEW.md'
    manifest_path = base / ('output/manifest.json' if kiosk else 'manifest.json')
    review_ref = ref(review, review_sha)
    manifest_ref = ref(manifest_path, manifest_sha)
    text = review.read_text()
    n.a.need(re.search(r'recommended only for (?:the )?isolated', text[:600].lower()) is not None and 'HOLD' not in text[:600] and
             'withdrawn' not in text[:600].lower(), 'Coordinator has not recommended final isolated source')
    manifest = n.load(manifest_path)
    dependencies = source_files(base, manifest, kiosk)
    dependencies[manifest_ref['path']] = manifest_ref
    registration_path = base / ('output/registration.json' if kiosk else 'registration.json')
    registration_ref = ref(registration_path)
    dependencies[registration_ref['path']] = registration_ref
    if kiosk:
        n.a.need(registration_ref['sha256'] in text and manifest_ref['sha256'] in text,
                 'Kiosk review must acknowledge current registration and manifest hashes')
    return review_ref, sorted(dependencies.values(), key=lambda row: row['path'])


def assemble(kiosk_review_sha, kiosk_manifest_sha, context_review_sha, context_manifest_sha):
    n.a.need(n.sha(n.ROOT / n.HARNESS) == FROZEN_SWIFT, 'Frozen Swift changed after coordinator build')
    kiosk, context = HERE / 'kiosk', HERE / 'context'
    kiosk_review, kiosk_deps = approval(kiosk, kiosk_review_sha, kiosk_manifest_sha, True)
    context_review, context_deps = approval(context, context_review_sha, context_manifest_sha, False)
    kiosk_reg = n.load(kiosk / 'output/registration.json')
    rows = n.load(context / 'registration.json')
    n.a.need(len(rows) == 4 and len({row['solidID'] for row in rows}) == 4, 'Exact four context registration rows required')
    sources, buildings = [], []
    for role, solid_id in n.TARGETS.items():
        is_kiosk = role == 'kiosk'
        row = kiosk_reg if is_kiosk else next(row for row in rows if row['solidID'] == solid_id)
        if is_kiosk:
            n.a.need('groundPixelsTopLeft' in row, 'Kiosk author must provide explicit authoritative groundPixelsTopLeft')
            pixels = row['groundPixelsTopLeft']
            image = ref(kiosk / 'output/source-full.png')
            n.a.need(image['sha256'] in (kiosk / 'COORDINATOR-REVIEW.md').read_text(), 'Kiosk image differs from coordinator-reviewed bytes')
        else:
            landmarks = row['geometryLandmarks']
            n.a.need([v['name'] for v in landmarks] == ['footprint-' + str(i) for i in range(4)], 'Wrong explicit context ground-corner ordering')
            solid = next(s for s in n.v5.authority()['solids'] if s['id'] == solid_id)
            n.a.need([v['worldXYZ'] for v in landmarks] == [v + [0] for v in n.vertices(solid)], 'Context source corners differ from authoritative bounds')
            pixels = [v['sourcePixelsTopLeft'] for v in landmarks]
            image = ref(n.a.safe(context, row['source']), row['sha256'])
        source = dict(role=role, status='recommended', image=image,
                      registration={key: row[key] for key in FIELDS},
                      dependencies=kiosk_deps if is_kiosk else context_deps,
                      recommendation=dict(reviewerRole='coordinator', decision='recommended', scope='isolated-ordinary-scene',
                                          sourceSHA256=image['sha256'], evidence=kiosk_review if is_kiosk else context_review))
        binding = dict(role=role, solidID=solid_id, nodeName=n.node_name(solid_id), groundPixelsTopLeft=pixels)
        n.a.need(row['solidID'] == solid_id, 'Wrong author solid identity')
        if not is_kiosk:
            n.a.need(row['nodeName'] == binding['nodeName'], 'Wrong context node identity')
        # Independent four-corner D108 check and exact image dimensions/hash.
        n.validate_building(source, binding)
        sources.append(source); buildings.append(binding)
    return dict(schema='building-perspective-recommendations-007', sources=sources, buildings=buildings)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    for role in ('kiosk', 'context'):
        parser.add_argument('--' + role + '-review-sha256', required=True)
        parser.add_argument('--' + role + '-manifest-sha256', required=True)
    parser.add_argument('--output', type=Path, default=HERE / 'recommendations.json')
    args = parser.parse_args()
    try:
        n.a.need(not args.output.exists(), 'Preserve existing recommendation binding')
        result = assemble(args.kiosk_review_sha256, args.kiosk_manifest_sha256,
                          args.context_review_sha256, args.context_manifest_sha256)
        args.output.write_text(json.dumps(result, indent=2) + '\n')
        print(json.dumps(dict(output=str(args.output), sha256=n.sha(args.output), sources=5,
                             sourceSHA256={s['role']: s['image']['sha256'] for s in result['sources']},
                             dependencyCounts={s['role']: len(s['dependencies']) for s in result['sources']},
                             nativeEvidence=False), indent=2))
    except (ValueError, OSError, KeyError, TypeError, StopIteration) as error:
        parser.exit(2, str(error) + '\n')


if __name__ == '__main__':
    main()
