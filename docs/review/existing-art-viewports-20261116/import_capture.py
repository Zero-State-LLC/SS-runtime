#!/usr/bin/env python3
"""Read-only xcresult import and gallery, requires existing exported attachments.
Usage: python3 -B import_capture.py RESULT.xcresult EXPORTS OUTPUT_DIRECTORY
Never executes a native test or modifies Swift. Refuses to replace an output packet.
"""
import hashlib
import html
import json
from pathlib import Path
import shutil
import subprocess
import sys
import verify_export as verifier


def run(result, exports, output):
    result, exports, output = map(lambda p: Path(p).resolve(), (result, exports, output))
    if output.exists():
        raise ValueError('Refusing to replace retained output')
    def fetch(section):
        raw = subprocess.check_output(['xcrun', 'xcresulttool', 'get', 'test-results', section,
                                       '--path', str(result), '--format', 'json'])
        return raw, json.loads(raw)
    summary_bytes, summary = fetch('summary')
    tree_bytes, tree = fetch('tests')
    report = verifier.verify(summary, tree, exports)
    output.mkdir(parents=True)
    shutil.copytree(exports, output / 'exports')
    (output / 'summary.json').write_bytes(summary_bytes)
    (output / 'tests.json').write_bytes(tree_bytes)
    report['xcresultPath'] = str(result)
    report['testIdentity'] = verifier.TEST
    (output / 'verification.json').write_text(json.dumps(report, indent=2) + '\n')
    manifest = json.loads((exports / 'manifest.json').read_text())
    plates, record = {}, None
    for case in manifest:
        for item in case['attachments']:
            raw = item['suggestedHumanReadableName']
            name = verifier.re.sub(r'_\d+_[0-9A-Fa-f-]{36}(?=\.(?:png|json)$)', '', raw)
            stem = name.removesuffix('.png').removesuffix('.json')
            if stem in verifier.EXPECTED:
                plates[stem] = item['exportedFileName']
            elif stem == 'existing-art-viewports-records':
                record = json.loads((exports / item['exportedFileName']).read_text())
    (output / 'records.json').write_text(json.dumps(record, indent=2) + '\n')
    cards = []
    for capture in record['captures']:
        name = capture['attachment']
        w, h = capture['pixels']
        detail = {k:v for k,v in capture.items() if k not in ('sha256', 'attachment')}
        cards.append(f'<section><h2>{html.escape(name)}</h2><pre>{html.escape(json.dumps(detail, indent=2))}</pre>'
            f'<div class="scroll"><img src="exports/{plates[name]}" width="{w}" height="{h}" '
            f'style="--w:{w}px;--h:{h}px" alt="{html.escape(name)}"></div></section>')
    page = '''<!doctype html><meta charset="utf-8"><title>Existing-art viewport diagnostic</title>
<style>body{font:16px sans-serif;background:#24282b;color:#eee;margin:24px}section{border-top:1px solid #aaa;padding:16px 0}pre{white-space:pre-wrap}.scroll{overflow:auto;max-width:100%}img{display:block;width:var(--w);height:var(--h);max-width:none}body.half img{width:calc(var(--w) / 2);height:calc(var(--h) / 2)}button{padding:12px}</style>
<h1>Existing-art viewport diagnostic, actual0653 simulator capture</h1>
<p>Technical export verified, visual acceptance UNREVIEWED. No physical device, VoiceOver, live cadence or coherent-source acceptance.</p>
<p>Native means one captured pixel per CSS pixel, NOT hardware size. Scene images are offscreen aspect-fit node renders. Hosted images use requested-size output canvases; actual UIKit bounds below can differ, causing clipping/unused canvas. Do not equate requested844 canvas with an observed844 host.</p>
<button onclick="document.body.classList.toggle('half')">Toggle native / half size</button>
'''
    (output / 'index.html').write_text(page + '\n'.join(cards))
    hashes = {str(p.relative_to(output)): hashlib.sha256(p.read_bytes()).hexdigest()
              for p in sorted(output.rglob('*')) if p.is_file()}
    (output / 'files-sha256.json').write_text(json.dumps(hashes, indent=2) + '\n')
    print(json.dumps(report, indent=2))

if __name__ == '__main__':
    run(*sys.argv[1:])
