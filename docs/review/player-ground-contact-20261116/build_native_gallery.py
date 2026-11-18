#!/usr/bin/env python3
"""Pair retained native attachments without changing any capture bytes."""
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent


def pairs():
    records = json.loads((HERE / 'native/native-records.json').read_text())['records']
    images = [r for r in records if r.get('image')]
    baseline = [r for r in images if r['family'] == 'baseline']
    result = []
    for row in baseline:
        matches = [r for r in images if r['family'] == 'weight-transfer'
                   and all(r[k] == row[k] for k in ('trace', 'policy', 'sample', 'frame'))]
        if len(matches) != 1:
            raise ValueError('Missing or duplicate native pair')
        other = matches[0]
        for record in (row, other):
            if not (HERE / 'native' / (record['image'] + '.png')).is_file():
                raise ValueError('Missing retained capture')
        result.append({k: row[k] for k in ('trace', 'policy', 'sample', 'tick', 'frame')} |
                      {'baseline': row['image'] + '.png', 'candidate': other['image'] + '.png'})
    if len(result) != 38 or len(images) != 76:
        raise ValueError('Expected exactly38 paired native captures')
    return result


def build():
    payload = json.dumps(pairs(), separators=(',', ':'))
    html = '''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width">
<title>South contact: static native pairs</title><style>
body{background:#252d32;color:#eee;font:16px system-ui;margin:24px;max-width:1100px}label{display:inline-block;margin:8px}select{max-width:95vw}section{display:flex;flex-wrap:wrap;gap:24px}figure{margin:12px 0}img{width:320px;height:220px;object-fit:contain;background:#303a3c}body.gray img{filter:grayscale(1)}body.half img{width:80px;height:55px}body.native img{width:160px;height:110px}p{line-height:1.5}#error{color:#ffb8a0}</style>
<h1>South contact: static native pairs</h1><p>Active: corrected looped-control run, November16 04:28UTC, <code>ss-groundcontact-native-20261116-0428-looped.xcresult</code>. The earlier clamped fixed-time attempt is invalid and retained only under <code>attempts/01-fixed-time-clamped/</code>. No movement policy is adopted.</p><p>38 paired explicit SpriteKit renders. These are static native crops, not displayed callback cadence, continuous contact pixels, Reduced Motion or device evidence. Contact spans use source landmarks projected through the native scene. The candidate changes recovery rise, not feet or world speed.</p>
<p><a href="README.md">Evidence and limits</a> · <a href="native-results.md">Measured native-scene spans</a> · <a href="normal-speed.html">Source normal</a> · <a href="quarter-speed.html">Source quarter</a></p>
<label>Paired capture <select id="pair"></select></label><label>Size <select id="size"><option value="large">2× logical crop</option><option value="native">Native logical crop</option><option value="half">Half logical crop</option></select></label><label><input type="checkbox" id="gray"> Grayscale</label>
<p id="status" aria-live="polite"></p><p id="error" role="alert"></p><section><figure><figcaption>Unchanged source control</figcaption><img id="baseline" alt="Baseline native crop"></figure><figure><figcaption>Proposed recovery weight transfer</figcaption><img id="candidate" alt="Candidate native crop"></figure></section>
<script>const pairs=PAYLOAD;const $=id=>document.getElementById(id);let generation=0;
for(const [i,p] of pairs.entries()){const option=document.createElement('option');option.value=i;option.textContent=`${p.trace} / ${p.policy} / sample${p.sample} / pose${p.frame+1}`;$('pair').append(option);}
async function render(){const token=++generation,p=pairs[Number($('pair').value)];document.body.dataset.ready='false';$('error').textContent='';$('status').textContent=`${p.trace} / ${p.policy} / sample${p.sample} / tick${p.tick} / pose${p.frame+1}`;
try{await Promise.all(['baseline','candidate'].map(family=>new Promise((resolve,reject)=>{const image=new Image();image.onload=()=>{if(!image.naturalWidth){reject(Error('Empty image'));return;}if(token===generation)$(family).src=image.src;resolve();};image.onerror=()=>reject(Error('Cannot load '+p[family]));image.src='native/'+p[family];})));if(token===generation)document.body.dataset.ready='true';}catch(e){if(token===generation)$('error').textContent='FAILED: '+e;}}
function style(){document.body.className=$('size').value+($('gray').checked?' gray':'');}
$('pair').onchange=render;$('size').onchange=$('gray').onchange=style;window.nativeContactReview={pairs,render};render();
</script></html>'''.replace('PAYLOAD', payload)
    (HERE / 'native-pairs.html').write_text(html)
    print('Built38 pairs from76 retained native attachments')


if __name__ == '__main__':
    build()
