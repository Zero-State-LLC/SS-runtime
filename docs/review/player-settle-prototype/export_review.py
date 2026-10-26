from pathlib import Path
from PIL import Image,ImageDraw
import json,hashlib,subprocess
R=Path(__file__).resolve().parent;root=R.parents[1];D=R/'review-frames';D.mkdir(exist_ok=True)
move=[Image.open(root/'outputs/SS-player-bounded-proportions/frames'/f'{i:02d}.png').convert('RGBA') for i in range(16)]
neutral=Image.open(root/'outputs/SS-player-bounded-neutral/frames/00.png').convert('RGBA')
settles={i:[Image.open(R/f'phase-{i:02d}/frames'/f'{k:02d}.png').convert('RGBA') for k in range(17)] for i in [5,13]}
checks=[]
for phase,ims in settles.items():
 assert ims[0].tobytes()==move[phase-1].tobytes()
 assert ims[-1].tobytes()==neutral.tobytes()
 checks.append({'phase':phase,'firstFrameExactMovement':True,'lastFrameExactNeutral':True,'distinctFrames':len({hashlib.sha256(im.tobytes()).hexdigest() for im in ims})})
for t in range(112):
 out=Image.new('RGB',(1536,448),'#30373b');d=ImageDraw.Draw(out)
 for col,(phase,kind) in enumerate([(5,'direct'),(5,'settle'),(13,'direct'),(13,'settle')]):
  release=32+phase
  if t<release:im=move[t%16]
  elif kind=='direct':im=neutral
  else:im=settles[phase][min(16,t-release+1)]
  out.paste(im,(col*384,32),im);d.text((col*384+12,12),f'Phase {phase}: {kind} | SOURCE ONLY',fill='white')
 out.save(D/f'{t:03d}.png')
for speed,fps in [('normal',32),('quarter',8)]:
 subprocess.run(['/opt/homebrew/bin/ffmpeg','-y','-v','error','-framerate',str(fps),'-i',str(D/'%03d.png'),'-c:v','libx264','-pix_fmt','yuv420p',str(R/f'{speed}-speed.mp4')],check=True)
(R/'export-checks.json').write_text(json.dumps({'framesPerVideo':112,'normalFPS':32,'quarterFPS':8,'endpoints':checks,'limits':['Source-only stationary root; not real-renderer footage','Half-second settling remains proposed','No gameplay input delay']},indent=2)+'\n')
print(checks)
