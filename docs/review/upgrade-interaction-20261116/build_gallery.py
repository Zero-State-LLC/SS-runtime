#!/usr/bin/env python3
"""Seal retained export bytes and build an orientation-aware diagnostic gallery."""
import html
import json
from pathlib import Path
import verify as v

HERE = Path(__file__).resolve().parent
capture = HERE / 'capture'
manifest = v.load(capture / 'manifest.json')
names = {item['exportedFileName'] for case in manifest for item in case['attachments']}
names |= {'summary.json', 'tests.json', 'manifest.json'}
(capture / 'inventory.json').write_text(json.dumps({name: v.sha(capture / name) for name in sorted(names)}, indent=2) + '\n')
rows = v.verify()
sections = []
for row in rows:
    record = row['record']
    figures = ''.join(f'<figure><figcaption>{stage}</figcaption><img src="capture/{name}" alt="{html.escape(record["dynamicTypeArgument"])} {stage}"></figure>' for stage, name in row['images'].items())
    sections.append(f'<section><h2>{html.escape(record["dynamicTypeArgument"])}</h2><p>{record["swipes"]} actual swipes. {html.escape(record["selectionResult"])}. AX label: {html.escape(record["accessibilityLabel"])}</p>{figures}</section>')
(HERE / 'index.html').write_text('''<!doctype html><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Actual upgrade interaction evidence</title><style>body{background:#202830;color:#eee;font:16px system-ui;margin:24px}section{border-top:1px solid #777;margin-top:24px}figure{margin:20px 0}img{display:block;width:667px;max-width:100%;height:auto;image-orientation:from-image}body.half img{width:333.5px}body.gray img{filter:grayscale(1)}button{padding:8px;margin-right:8px}</style><h1>Actual upgrade interactions</h1><p>Three passing XCUI tests on SE3 simulator. Unmodified production view in isolated host. Not physical VoiceOver, full-game resume, or visual acceptance. Screen captures honor original EXIF orientation. Initial cropped window-capture attempt retained separately.</p><button onclick="document.body.classList.toggle('half')">Native / half</button><button onclick="document.body.classList.toggle('gray')">Grayscale</button>''' + ''.join(sections))
print('Sealed15 retained files; built9-image gallery. Hashes attest retained bytes, not executed source.')
