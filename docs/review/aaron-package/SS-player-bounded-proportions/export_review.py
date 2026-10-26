from pathlib import Path
from PIL import Image,ImageDraw
import numpy as np,json,hashlib
R=Path(__file__).resolve().parent;B=R.parent/'SS-player-low-recovery'
frames=[Image.open(R/'frames'/f'{i:02d}.png').convert('RGBA') for i in range(16)]
flat=[]
for im in frames:
 b=Image.new('RGBA',im.size,'#283036');b.alpha_composite(im);flat.append(b.convert('RGB'))
for name,dur in [('normal-speed',31.25),('quarter-speed',125)]:
 flat[0].save(R/(name+'.png'),save_all=True,append_images=flat[1:],duration=dur,loop=0,format='PNG')
 # GIF centisecond quantization distributed over cycle, not mislabeled uniform timing.
 timing=[round((i+1)*dur/10)*10-round(i*dur/10)*10 for i in range(16)]
 flat[0].save(R/(name+'.gif'),save_all=True,append_images=flat[1:],duration=timing,loop=0)
 ms=500 if name=='normal-speed' else 2000
 title='Normal speed · 0.5-second loop' if ms==500 else 'Quarter speed · 2-second loop'
 html='''<!doctype html><meta charset="utf-8"><meta name="viewport" content="width=device-width"><title>Player material detail — TITLE</title><style>body{background:#192026;color:#e2dfd6;font:16px system-ui;margin:32px auto;max-width:960px;padding:0 20px}a{color:#d0b987}canvas{background:#283036;max-width:100%;height:auto}button{padding:9px;margin:10px 6px 10px 0}small{color:#b5b9b9}</style><h1>TITLE</h1><p>Material-only comparison: restored source contrast on calf and boots. Preferred narrow stance and arm swing retained. Source candidate; dimensions, amplitudes and hidden surfaces remain proposed.</p><nav><a href="normal-speed.html">Normal speed only</a> · <a href="quarter-speed.html">Quarter speed only</a> · <a href="detail-review.png">Detail comparison</a> · <a href="seam-review.png">16→1 seam</a></nav><p><button id="toggle">Pause</button><button id="next">Next frame</button><span id="frame"></span></p><canvas width="384" height="448"></canvas><p><small>Source-detail preview; display scales to fit the panel. Production size remains undecided. Canvas uses the same 16 PNGs with a CYCLE ms cycle; this is source playback, not live-renderer motion.</small></p><script>const c=document.querySelector('canvas'),x=c.getContext('2d'),ims=[];let start=0,playing=true,f=0;Promise.all(Array.from({length:16},(_,i)=>new Promise(r=>{let im=new Image;im.onload=()=>{ims[i]=im;r()};im.src='frames/'+String(i).padStart(2,'0')+'.png'}))).then(()=>{start=performance.now();requestAnimationFrame(tick)});function draw(){if(!ims[f])return;x.fillStyle='#283036';x.fillRect(0,0,768,448);x.drawImage(ims[f],0,16);document.querySelector('#frame').textContent='Frame '+(f+1)+' / 16'}function tick(t){if(playing)f=Math.floor((Math.max(0,t-start)%CYCLE)/CYCLE*16);draw();requestAnimationFrame(tick)}document.querySelector('#toggle').onclick=()=>{playing=!playing;start=performance.now()-f*CYCLE/16;document.querySelector('#toggle').textContent=playing?'Pause':'Play'};document.querySelector('#next').onclick=()=>{playing=false;f=(f+1)%16;document.querySelector('#toggle').textContent='Play';draw()};</script>'''.replace('TITLE',title).replace('CYCLE',str(ms))
 (R/(name+'.html')).write_text(html)
plate=Image.new('RGB',(1536,930),'#283036');d=ImageDraw.Draw(plate)
for col,i in enumerate([0,4,8,12]):
 for row,root in enumerate([B,R]):
  im=Image.open(root/'frames'/f'{i:02d}.png').convert('RGBA');bg=Image.new('RGBA',im.size,'#283036');bg.alpha_composite(im)
  crop=bg.crop((112,190,272,400)).resize((320,420));plate.paste(crop,(col*384+32,row*465+35));d.text((col*384+20,row*465+12),f'{"BEFORE" if row==0 else "MATERIAL DETAIL"} — frame {i+1:02d}',fill='white')
plate.save(R/'detail-review.png')
seam=Image.new('RGB',(1536,450),'#283036');d=ImageDraw.Draw(seam)
for col,i in enumerate([14,15,0,1]):seam.paste(flat[i],(col*384,30));d.text((col*384+12,10),f'Frame {i+1}',fill='white')
seam.save(R/'seam-review.png')
rows=[]
for i in range(16):
 a=np.array(flat[i]).astype(float);b=np.array(flat[(i+1)%16]).astype(float);rows.append({'from':i+1,'to':(i+1)%16+1,'meanAbsoluteRGBDifference':float(abs(a-b).mean())})
assert (R/'source/samples.json').read_bytes()==(R/'boot/samples.json').read_bytes()

assert len({hashlib.sha256(im.tobytes()).hexdigest() for im in frames})==16
for im in frames:assert im.size==(384,416) and im.getbbox()[0]>0 and im.getbbox()[2]<384 and im.getbbox()[3]<416
report={'status':'SOURCE_POLISH_CANDIDATE_NOT_ADMITTED','unchangedPoseSamples':True,'frameCount':16,'uniqueFrames':16,'canvas':[384,416],'normalCycleSeconds':.5,'quarterCycleSeconds':2,'armControlsUnchanged':{'elbowPixels':4,'handPixels':10},'gloveChange':'rigid translation below wrist; sleeve deformation above wrist','transitions':rows,'limits':['No live-travel evidence','One facing only','Hidden material and knee-cap finish proposed','Difference statistics are not visual acceptance']}
(R/'polish-verification.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
