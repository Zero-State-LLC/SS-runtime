#!/usr/bin/env python3
"""Generate revision02 gallery without modifying any capture bytes."""
from pathlib import Path
import json
HERE = Path(__file__).resolve().parent

def build():
    records = json.loads((HERE/'capture/r02-records.json').read_text())
    assert len(records['captures']) == 18
    options = '\n'.join(f'<option value="{c["name"]}">{c["name"]}</option>' for c in records['captures'])
    html = '''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Revision02 bound-input baseline</title><style>body{font:16px system-ui;background:#202529;color:#eee;margin:20px;overflow-x:hidden}a{color:#9cdbed}.panel{overflow:auto;max-width:calc(100vw - 48px);width:fit-content}img{display:block;max-width:none}select{max-width:100%}.warning{color:#ffd28a}</style>
<h1>Revision02: fresh bound-input baseline, NOT visual acceptance</h1>
<p class="warning">ORDINARY is primary. STAGED is secondary art-only, with HUD and field suppressed. Building NOT SOLVED, paving seam/repetition pending, soft shadows absent, production HUD and authoritative field prominence open.</p>
<p><a href="README.md">Evidence, exact limits and commands</a> | <a href="../coverage.md">Game-wide coverage (not expanded by this fixture)</a> | <a href="../../visual-acceptance-20261116/CONTRACT.md">Visual acceptance contract</a></p>
<label>Capture <select id="capture">OPTIONS</select></label>
<label>Sheet <select id="sheet"><option>native</option><option>half</option><option>grayscale</option></select></label><p id="note"></p>
<h2>Fixed approved concept, normalized reference</h2><p>Original 1672x941, aspect preserved, different aspect and framing. Not a renderer output. Grayscale is CSS only, original bytes unchanged.</p><div class="panel"><img id="benchmark" src="../../bp001-decision-20261116/street-corner-approved-concept.png" alt="Fixed approved benchmark"></div>
<h2>Actual SpriteKit capture</h2><div class="panel"><img id="plate" alt="Revision02 actual native capture"></div>
<script>const q=id=>document.getElementById(id);function show(){const n=q('capture').value,s=q('sheet').value,w=s==='half'?352:704,h=s==='half'?163:326;const p=q('plate');p.src='capture/'+n+'-'+s+'.png';p.style.width=w+'px';p.style.height=h+'px';const b=q('benchmark');b.style.width=w+'px';b.style.height='auto';b.style.filter=s==='grayscale'?'grayscale(1)':'none';q('note').textContent=n.includes('-staged-')?'STAGED SECONDARY: HUD and field suppressed, not gameplay field-off.':'ORDINARY PRIMARY: production HUD and authoritative field retained.';document.body.dataset.selection=n+'-'+s;}q('capture').onchange=show;q('sheet').onchange=show;show();</script></html>'''.replace('OPTIONS', options)
    (HERE/'index.html').write_text(html)
    print('Gallery: 18 capture selections x 3 sheets, native 704x326, half 352x163')

if __name__ == '__main__': build()
