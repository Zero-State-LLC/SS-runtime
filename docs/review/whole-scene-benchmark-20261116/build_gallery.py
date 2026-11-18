#!/usr/bin/env python3
"""Build the portable whole-scene gallery and the game-wide coverage matrix from retained evidence.
Read-only over capture/. Never writes plates. Coverage rows cite existing paths only."""
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
REVIEW = HERE.parent
BENCHMARK = '../bp001-decision-20261116/street-corner-approved-concept.png'
UNSOLVED = [('Building', 'NOT SOLVED: building-constrained.png fallback. The new stone facade is pending registration and not integrated.'),
            ('Paving material', 'NOT SOLVED: beige env_ground_plaza retained. Only the pavement width changed.'),
            ('Soft contact shadows', 'ABSENT: none supplied, none authored.'),
            ('HUD prominence', 'OPEN: production HUD unchanged.'),
            ('Camera field prominence', 'OPEN: authoritative cone unchanged. .paired contrast and zoom are diagnostics only.')]

# (row, captured?, technical, evidence path relative to docs/review or None, note)
COVERAGE = [
    ('Quiet street, control vs diagnostic', True, 'verified (verify_capture + 7 offline)', 'whole-scene-benchmark-20261116/capture', 'This packet. Static only.'),
    ('Dense legal encounter (ghost-step tick4976)', True, 'verified in BP001 trial', 'bp001-reference-trial-20261116/plates', 'Previous art only; no whole-scene diagnostic arm.'),
    ('Hostile/legal projected framing', True, 'earlier capture', 'hostile-framing', 'Previous art.'),
    ('Occlusion: perimeter study', True, 'earlier capture', 'occlusion-perimeter/review.md', 'Test-only probe; front/rear/corner sides not separately covered for this scene.'),
    ('Occlusion: front/rear/corner, this scene', False, None, None, 'NOT CAPTURED.'),
    ('South movement contact (native static)', True, 'verified (verify_native + 14 offline)', 'player-ground-contact-20261116/native-results.md', 'Static renderer, not live.'),
    ('South release phases (native static)', True, 'verified', 'player-release-variation-native-20261116', 'Proposals, not accepted.'),
    ('North/east/west facings', True, 'source only', 'player-side-source-20261116', 'Source sheets; no native whole-scene capture.'),
    ('Camera integrity states / damage markers', True, 'earlier capture', 'camera-damage-markers/review.md', 'Not in this scene fixture.'),
    ('Camera field-off', True, 'staged view only', 'whole-scene-benchmark-20261116/capture', 'Staged presentation flag only, not a gameplay field-off state.'),
    ('Enemy roles (all existing)', False, None, None, 'NOT CAPTURED in this published coverage packet. Local first-sample source work is unpublished and is not evidence here. No native whole-scene capture of any enemy.'),
    ('Combat effects (hits, bolts, mines, telegraphs)', False, None, None, 'NOT CAPTURED in whole-scene review.'),
    ('UI states (pause, upgrade, results, lethal warning)', False, None, None, 'NOT CAPTURED in whole-scene review.'),
    ('Screen sizes / safe areas', True, 'measurements only', 'stable-hud-reservation/README.md', 'Not whole-scene visual.'),
    ('Accessibility (Reduced Motion, HUD scale, VoiceOver)', True, 'Reduced Motion only', 'reduced-motion-validation/README.md', 'HUD scale and VoiceOver whole-scene NOT CAPTURED.'),
    ('Live cadence', True, 'diagnostic, issue #237 open', 'live-playback/README.md', 'Not accepted; callback gaps remain.'),
    ('Physical device', False, None, None, 'NOT CAPTURED for this scene. device-qa notes are code reads, not captures.'),
]

def plate(arm, mode, zoom, sheet): return f'capture/wholescene-{arm}-{mode}-z{zoom}-{sheet}.png'

def build():
    for arm in ('control', 'diagnostic'):
        for mode in ('ordinary', 'staged'):
            for zoom in (100, 125, 140):
                for sheet in ('native', 'half', 'grayscale'):
                    assert (HERE / plate(arm, mode, zoom, sheet)).is_file()
    for row in COVERAGE:
        if row[3]: assert (REVIEW / row[3]).exists(), row[3]
    status = ''.join(f'<li><b>{k}:</b> {v}</li>' for k, v in UNSOLVED)
    html = f'''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Whole-scene benchmark comparison</title>
<style>body{{font:15px system-ui;background:#1d2326;color:#eee;margin:20px}}a{{color:#9cdbed}}.row{{display:flex;gap:12px;flex-wrap:wrap}}
figure{{margin:0;flex:0 0 auto;max-width:100%}}.panel{{overflow:auto;max-width:calc(100vw - 48px);outline:1px solid #556;width:fit-content}}img{{display:block;border:0}}.warn{{background:#5a2b1f;padding:8px 12px;border-radius:4px}}
body{{overflow-x:hidden}}.row{{flex-direction:column}}
label{{margin-right:14px}}#mode-note{{color:#ffd28a}}</style>
<h1>Whole-scene benchmark: fixed benchmark vs control vs diagnostic</h1>
<p class="warn" id="status"><b>DIAGNOSTIC, NOT A CORRECTION, NOT VISUAL ACCEPTANCE.</b> Byte identity is provenance only.</p>
<ul id="unsolved">{status}</ul>
<p><a href="README.md">Evidence and limits</a> · <a href="coverage.md">Game-wide coverage matrix</a> · <a href="../visual-acceptance-20261116/CONTRACT.md">Visual acceptance contract</a></p>
<label>View <select id="mode"><option value="ordinary" selected>ORDINARY (primary): HUD and field visible</option><option value="staged">STAGED (secondary): HUD and field hidden, art-only</option></select></label>
<label>Zoom <select id="zoom"><option>100</option><option selected>125</option><option>140</option></select></label>
<label>Sheet <select id="sheet"><option value="native" selected>native</option><option value="half">50%</option><option value="grayscale">grayscale</option></select></label>
<p id="mode-note"></p>
<div class="row">
<figure><figcaption>Fixed approved benchmark: <b>normalized reference</b> (read-only, SHA 49aa3544…, original 1672×941, scaled to the capture width with aspect preserved; different aspect, not identical framing, not a renderer output)</figcaption><div class="panel"><img id="benchmark" src="{BENCHMARK}" alt="Approved concept benchmark"></div></figure>
<figure><figcaption id="cap-control">Control (midpoint, existing art)</figcaption><div class="panel"><img id="control" alt="Control capture"></div></figure>
<figure><figcaption id="cap-diagnostic">Diagnostic (roadway placement and pavement width only)</figcaption><div class="panel"><img id="diagnostic" alt="Diagnostic capture"></div></figure>
</div>
<p id="error"></p>
<script>
'use strict';
const $=id=>document.getElementById(id);
const SIZE={{native:[704,326],half:[352,163],grayscale:[704,326]}};
function show(){{
  const m=$('mode').value,z=$('zoom').value,s=$('sheet').value,[w,h]=SIZE[s];
  $('mode-note').textContent = m==='staged' ? 'STAGED (secondary): suppressed for art-only review: production HUD hidden (isHidden), Camera field hidden (presentation fieldVisible=false). Simulation unchanged. Do not judge legibility from this view.' : 'ORDINARY: primary view with production HUD and authoritative Camera field.';
  for(const arm of ['control','diagnostic']){{const img=$(arm);img.style.width=w+'px';img.style.height=h+'px';img.onerror=()=>{{$('error').textContent='Missing capture: '+img.src;document.body.dataset.ready='false';}};img.src=`capture/wholescene-${{arm}}-${{m}}-z${{z}}-${{s}}.png`;$('cap-'+arm).dataset.current=`${{arm}}-${{m}}-z${{z}}-${{s}}`;}}
  const b=$('benchmark');b.style.width=w+'px';b.style.height='auto';b.style.filter=s==='grayscale'?'grayscale(1)':'none';
  document.body.dataset.selection=`${{m}}-z${{z}}-${{s}}`;
}}
for(const id of ['mode','zoom','sheet'])$(id).onchange=show;
show(); document.body.dataset.ready='true';
</script></html>
'''
    (HERE / 'index.html').write_text(html)
    lines = ['# Game-wide visual coverage matrix', '',
             'Every visual row is **NOT ACCEPTED**: no owner visual acceptance has been recorded for any of them. "Technical" describes how the evidence was verified, not its quality. Rows marked NOT CAPTURED have no evidence. The quiet fixture does not stand in for any other row.', '',
             '| Row | Captured | Technical | Visual | Evidence (docs/review/) | Note |', '|---|---|---|---|---|---|']
    for name, captured, technical, path, note in COVERAGE:
        lines.append(f"| {name} | {'captured' if captured else 'NOT CAPTURED'} | {technical or '—'} | NOT ACCEPTED | {f'`{path}`' if path else '—'} | {note} |")
    (HERE / 'coverage.md').write_text('\n'.join(lines) + '\n')
    print('Wrote index.html and coverage.md:', len(COVERAGE), 'rows')

if __name__ == '__main__': build()
