from pathlib import Path
import json,sys,math,numpy as np
from PIL import Image
from thigh import render_thigh
R=Path(__file__).resolve().parent;S=R/'source';rig=json.loads((S/'body-rig.json').read_text());rows=[]
for frame in json.loads((S/'samples.json').read_text()):
 for pose in frame['legs']:
  side=pose['side'];paint=Image.open(S/'body-source'/f'{side}_thigh.png').convert('RGBA')
  im,depth=render_thigh(pose,paint,rig['bones'][side+'_hip']['pivot'],rig['bones'][side+'_knee']['pivot'])
  x,y,z=pose['knee'];px=round(192+6*x);py=round(336+6*(.5*y-math.sqrt(.75)*z));center_depth=y*math.sqrt(.75)+z*.5
  alpha=np.array(im)[py,px,3];visible_depth=float(depth[py,px]);assert alpha==255 and math.isfinite(visible_depth) and visible_depth>center_depth
  rows.append({'time':frame['time'],'side':side,'jointCenterPixel':[px,py],'alpha':int(alpha),'frontSurfaceDepthAboveJointCenter':visible_depth-center_depth})
(R/'joint-verification.json').write_text(json.dumps(rows,indent=2)+'\n');print('32 projected knee centers covered by finite, opaque joint/thigh surface in front of source joint center.')
