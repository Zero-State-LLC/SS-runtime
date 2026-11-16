#!/usr/bin/env python3
"""Source-only contact comparison pages driven by executed Swift trace samples."""
import json
from pathlib import Path
HERE = Path(__file__).resolve().parent

def export():
    source = json.loads((HERE/'contact-comparison.json').read_text())
    records = []
    for result in source['results']:
        records.append({'scenario': result['scenario'], 'policy': result['policy'], 'rows': [
            {k: row[k] for k in ('sample','tick','xRaw','yRaw','frame','paused','dodgeRemaining')}
            for row in result['rows']]})
    payload = json.dumps(records, separators=(',', ':'))
    template = r'''<!doctype html><meta charset="utf-8"><title>BP-008 source contact comparison</title>
<style>body{background:#20272a;color:#eee;font:16px system-ui;margin:24px}a{color:#9cdbed}section{display:flex;gap:16px;flex-wrap:wrap}canvas{width:min(704px,100%);height:auto;border:1px solid #68747b}article{max-width:704px}button,select,input{font:inherit;margin:6px}p{max-width:1100px}#error{color:#ffc5ac}input[type=range]{width:500px;max-width:90%}</style>
<h1>South source contact comparison: RATE speed</h1>
<p><strong>Actual core travel, hypothetical exported-pose sampling. Not SpriteKit capture or live cadence.</strong> Same world trace, 0.5s source cycle, 64×69.333 logical art and original root registration in both columns. Existing 0.375s settling and approved releases5/13 are unchanged and not replayed here.</p>
<p><a href="normal-speed.html">Normal speed</a> · <a href="quarter-speed.html">Separate quarter speed</a> · <a href="first-findings.md">Trace findings</a> · <a href="README.md">Evidence and gates</a></p>
<label>Scenario <select id="scenario"></select></label><label>Phase model <select id="policy"><option>fixed-time</option><option>distance-phase</option></select></label>
<button id="play" disabled>Play</button><button id="reset">Start</button><label><input id="gray" type="checkbox">Grayscale</label>
<div><input id="scrub" type="range" min="0" value="0"><output id="status">Loading32 source frames…</output></div>
<p id="error"></p><p>Cardinal, wall-slide and reversal deliberately hold south source as a diagnostic, not an authored facing. No walk image is invented for idle/collision stop or dodge. Pause rows hold the core tick. Grid and crosshairs are annotations, never collision authority.</p>
<section><article><h2>Unchanged walk control</h2><canvas id="control" width="704" height="326"></canvas></article><article><h2>Bounded brisk recovery proposal</h2><canvas id="candidate" width="704" height="326"></canvas></article></section>
<p>Proposal: reduce recovery pelvis rise by at most0.6 source units using the existing fixed-length solver. All feet, planted intervals, speed and cycle duration remain identical. Six changed keys, no extra bounce, no increased cadence. Both columns therefore retain the same modeled support slip. Visual improvement is unreviewed.</p>
<script>
'use strict';
const records=PAYLOAD, rate=RATEVALUE;
const $=id=>document.getElementById(id), images=[[],[]];
let playing=false, origin=0, position=0, ready=false;
const scenarios=[...new Set(records.map(x=>x.scenario))];
for(const name of scenarios){const option=document.createElement('option');option.textContent=name;$('scenario').append(option);}
function selected(){return records.find(x=>x.scenario===$('scenario').value&&x.policy===$('policy').value);}
function draw(){const trace=selected(), row=trace.rows[position], first=trace.rows[0];$('scrub').max=trace.rows.length-1;$('scrub').value=position;
 $('status').textContent=`sample${row.sample} / tick${row.tick} / source pose${row.frame===null?'excluded':row.frame+1} / ${row.paused?'PAUSED':''}`;
 const dx=(row.xRaw-first.xRaw)/256,dy=(row.yRaw-first.yRaw)/256;
 const rootX=352+(dx-dy)/Math.sqrt(2),rootY=82-(dx+dy)/(2*Math.sqrt(2));
 for(let v=0;v<2;v++){const canvas=$(v?'candidate':'control'),ctx=canvas.getContext('2d');ctx.clearRect(0,0,704,326);ctx.fillStyle='#303a3c';ctx.fillRect(0,0,704,326);ctx.strokeStyle='#4a5657';ctx.lineWidth=1;
  for(let x=0;x<704;x+=20){ctx.beginPath();ctx.moveTo(x,0);ctx.lineTo(x,326);ctx.stroke();}
  for(let y=2;y<326;y+=20){ctx.beginPath();ctx.moveTo(0,y);ctx.lineTo(704,y);ctx.stroke();}
  ctx.strokeStyle='#e7c584';ctx.beginPath();ctx.moveTo(rootX-6,rootY);ctx.lineTo(rootX+6,rootY);ctx.moveTo(rootX,rootY-6);ctx.lineTo(rootX,rootY+6);ctx.stroke();
  if(row.frame!==null&&ready){ctx.save();ctx.filter=$('gray').checked?'grayscale(1)':'none';ctx.drawImage(images[v][row.frame],rootX-32,rootY-56,64,416/6);ctx.restore();}
  else{ctx.fillStyle='#fff';ctx.fillText('No walking pose: native idle/dodge/settle remains separate',18,300);}
  ctx.fillStyle='#fff';ctx.fillText(`authoritative Q8 ${row.xRaw},${row.yRaw}; source-model frame ${row.frame}`,18,22);
 }
}
function stop(){playing=false;$('play').textContent='Play';}
$('play').onclick=()=>{if(!ready)return;if(playing){stop();return;}playing=true;origin=performance.now()-position/60/rate*1000;$('play').textContent='Pause';};
$('reset').onclick=()=>{stop();position=0;draw();};
$('scrub').oninput=()=>{stop();position=Number($('scrub').value);draw();};
$('scenario').onchange=$('policy').onchange=()=>{stop();position=0;draw();};
$('gray').onchange=draw;
function animate(time){if(playing){position=Math.floor((time-origin)/1000*60*rate);if(position>=selected().rows.length){position=selected().rows.length-1;stop();}draw();}requestAnimationFrame(animate);}
Promise.all([0,1].flatMap(v=>Array.from({length:16},(_,i)=>new Promise((resolve,reject)=>{const image=new Image();images[v][i]=image;image.onload=()=>image.naturalWidth===384&&image.naturalHeight===416?resolve():reject(Error('canvas size'));image.onerror=()=>reject(Error(image.src));image.src=(v?'editable-candidate/frames/':'baseline-frames/')+String(i).padStart(2,'0')+'.png';})))).then(()=>{ready=true;document.body.dataset.ready='true';$('play').disabled=false;draw();requestAnimationFrame(animate);}).catch(error=>{$('error').textContent='FAILED: '+error;document.body.dataset.ready='false';});
window.contactReview={selected,draw,get ready(){return ready;},get position(){return position;}};
draw();
</script>'''
    for name, label, rate in [('normal-speed.html','normal',1),('quarter-speed.html','quarter',.25)]:
        html = template.replace('RATEVALUE',str(rate)).replace('PAYLOAD',payload).replace('RATE',label)
        (HERE/name).write_text(html)
    print('Exported two source-only pages with32 real painted frames and actual core rows')

if __name__=='__main__': export()
