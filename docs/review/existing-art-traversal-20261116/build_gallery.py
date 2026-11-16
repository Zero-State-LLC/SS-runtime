#!/usr/bin/env python3
"""Build gallery only from actual imported native records. No source pixels are edited."""
import html
import json
from pathlib import Path
import verify_capture as v
HERE=Path(__file__).resolve().parent

def build():
    v.need((HERE/'capture/eat-records.json').is_file(),'No actual native evidence: gallery not built')
    packet=v.load(HERE/'capture/eat-records.json')
    captures={c['name']:c for arm in packet['arms'] for c in arm['captures']}
    for name in captures: v.need((HERE/'capture'/f'{name}.png').is_file(),f'Missing actual capture:{name}')
    data=json.dumps(captures).replace('</','<\\/')
    options=''.join(f'<option>{html.escape(n)}</option>' for n in [name for name,_ in v.LEGS]+['pause'])
    page='''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Existing-art traversal, not repaired-scene acceptance</title>
<style>body{font:15px system-ui;background:#202529;color:#eee;margin:20px;overflow-x:hidden}a{color:#9cdbed}.warning{color:#ffd28a}.panel{overflow:auto;width:fit-content;max-width:calc(100vw - 48px)}img{display:block;max-width:none}figure{margin:18px 0}select{max-width:100%}pre{white-space:pre-wrap}</style>
<h1>Existing-art traversal: actual post-action keypoints</h1>
<p class="warning"><b>DIAGNOSTIC, NOT COHERENT REPAIRED SCENE OR VISUAL ACCEPTANCE.</b> Existing shipping art and test-position start only. World-side geometry is not complete visible-pixel occlusion proof. No device,16-pose or performance acceptance.</p>
<p><a href="README.md">Exact scope and native provenance</a> | <a href="../visual-acceptance-20261116/CONTRACT.md">Visual acceptance contract</a></p>
<label>Keypoint <select id="phase">OPTIONS</select></label>
<label>Mapping <select id="mapping"><option value="shipping">Shipping live tree, post-action still</option><option value="midpoint-post-action-still">Midpoint reversible post-action STILL, not live midpoint display</option></select></label>
<label>Size <select id="sheet"><option value="native">Native logical size</option><option value="half">50%</option><option value="grayscale">Grayscale</option></select></label>
<figure><figcaption>Original approved concept: width-normalized reference, original1672x941 aspect preserved, different framing. Not a renderer output.</figcaption><div class="panel"><img id="benchmark" src="../bp001-decision-20261116/street-corner-approved-concept.png" alt="Fixed approved benchmark"></div></figure>
<figure><figcaption>Normal setting, ordinary HUD and authoritative fields retained</figcaption><div class="panel"><img id="normal" alt="Actual normal-setting post-action keypoint"></div><pre id="normal-note"></pre></figure>
<figure><figcaption>Reduced Motion setting, same actual command stream</figcaption><div class="panel"><img id="reduced" alt="Actual Reduced Motion post-action keypoint"></div><pre id="reduced-note"></pre></figure>
<p class="warning">Midpoint capture transforms the same selected textures for a still and restores the tree before the next live update. It does not prove continuous midpoint playback, faithful sources or accepted contact/occlusion.</p>
<script>const captures=DATA,q=id=>document.getElementById(id);function show(){const p=q('phase').value,m=q('mapping').value,s=q('sheet').value,w=s==='half'?352:704,h=s==='half'?163:326;for(const arm of ['normal','reduced']){const name=`eat-${arm}-${p}-${m}`,c=captures[name],i=q(arm);i.src='capture/'+name+'.png';i.style.width=w+'px';i.style.height=h+'px';i.style.filter=s==='grayscale'?'grayscale(1)':'none';q(arm+'-note').textContent=JSON.stringify({tick:c.tick,digest:c.digest,actualSceneRoot:c.observedPlayerSceneRoot,imagePixels:c.nativePixels},null,2);}q('benchmark').style.width=w+'px';q('benchmark').style.height='auto';q('benchmark').style.filter=s==='grayscale'?'grayscale(1)':'none';document.body.dataset.selection=p+'-'+m+'-'+s;}for(const id of ['phase','mapping','sheet'])q(id).onchange=show;show();</script></html>'''
    (HERE/'index.html').write_text(page.replace('OPTIONS',options).replace('DATA',data))
    print(f'Built gallery from {len(captures)} actual captures;13 keypoints x2 mappings x3 display modes')

if __name__=='__main__': build()
