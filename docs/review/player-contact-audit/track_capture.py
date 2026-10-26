from pathlib import Path
import subprocess,json
import numpy as np
from PIL import Image,ImageDraw
ROOT=Path(__file__).resolve().parents[2]
OUT=Path(__file__).resolve().parent
video=ROOT/'outputs/SS-shared-traversal-recorded/standard-normal-detail.mp4'
raw=subprocess.check_output(['ffmpeg','-v','error','-i',str(video),'-fps_mode','passthrough','-f','rawvideo','-pix_fmt','rgb24','-'])
frames=np.frombuffer(raw,dtype=np.uint8).reshape(-1,840,400,3)
probes=[]
for i in range(16):
 im=Image.open(ROOT/f'work/SS-runtime/AppTests/BenchmarkAssets/player-source-s-{i:02d}.png').convert('RGBA').resize((192,208),Image.Resampling.BILINEAR)
 a=np.array(im); yy,xx=np.where((a[:,:,3]>253)&(np.indices(a.shape[:2])[0]>90))
 pick=np.linspace(0,len(xx)-1,160,dtype=int);yy,xx=yy[pick],xx[pick]
 probes.append((yy,xx,a[yy,xx,:3].astype(np.float32)))
records=[];last=None
for n,f in enumerate(frames):
 ylo,yhi=(130,420) if last is None else (max(0,last-14),min(631,last+15))
 ys,xs=np.meshgrid(np.arange(ylo,yhi),np.arange(117,127),indexing='ij');ys,xs=ys.ravel(),xs.ravel()
 candidates=[]
 for pose,(yy,xx,color) in enumerate(probes):
  pix=f[ys[:,None]+yy[None,:],xs[:,None]+xx[None,:]].astype(np.float32)
  scores=np.mean((pix-color[None,:,:])**2,axis=(1,2));j=int(np.argmin(scores))
  candidates.append((float(scores[j]),pose,int(xs[j]),int(ys[j])))
 candidates.sort();error,pose,x,y=candidates[0];last=y
 records.append(dict(movieFrame=n,pose=pose,x=x,y=y,mse=error,runnerUpMSE=candidates[1][0]))
(OUT/'pixel-match.json').write_text(json.dumps({'method':'Masked lower-body RGB template match against all 16 half-scale source rasters. Heuristic pixel identity, not ground-contact certification. Source opaque probes only; compression and subpixel rendering affect scores.','frames':records},indent=2)+'\n')
wraps=[n for n in range(1,len(records)) if records[n-1]['pose']>=14 and records[n]['pose']<=1]
print('frames',len(records),'poses',sorted({r['pose'] for r in records}),'wraps',wraps,'mse range',min(r['mse'] for r in records),max(r['mse'] for r in records))
for w in wraps:
 indices=list(range(max(0,w-3),min(len(records),w+4)))
 sheet=Image.new('RGB',(192*len(indices),238),(35,40,44));d=ImageDraw.Draw(sheet)
 for j,n in enumerate(indices):
  r=records[n];im=Image.fromarray(frames[n]).crop((r['x'],r['y'],r['x']+192,r['y']+208));sheet.paste(im,(j*192,30));d.text((j*192+4,5),f"video {n}; est. {r['pose']+1}; MSE {r['mse']:.0f}",fill='white')
 sheet.save(OUT/f'live-seam-{w}.png')
