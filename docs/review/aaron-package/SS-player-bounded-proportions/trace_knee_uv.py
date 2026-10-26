from pathlib import Path
import json
import numpy as np
from PIL import Image
R=Path(__file__).resolve().parent
s=(R/'thigh.py').read_text().replace(' v=np.array(vertices);screen=', ' uv_trace=np.full((size[1],size[0],3),-1.0)\n v=np.array(vertices);screen=')
s=s.replace('   rgb[sl][mask]=color[mask]','''   uv_trace[sl][mask]=-1
   if fi>=64 and front[fi]:
    selected=mask&cap
    uv_trace[sl][selected]=np.stack([sx,sy,color[:,:,:3].mean(axis=2)],axis=-1)[selected]
   rgb[sl][mask]=color[mask]''').replace(' return Image.fromarray(rgb),depth',' return Image.fromarray(rgb),depth,uv_trace')
ns={};exec(compile(s,'trace','exec'),ns)
rig=json.loads((R/'source/body-rig.json').read_text());poses=json.loads((R/'source/samples.json').read_text());rows=[]
for i in [0,2,6,8,10,14]:
 for p in poses[i]['legs']:
  side=p['side'];paint=Image.open(R/'source/body-source'/f'{side}_thigh.png').convert('RGBA')
  im,depth,uv=ns['render_thigh'](p,paint,rig['bones'][side+'_hip']['pivot'],rig['bones'][side+'_knee']['pivot'])
  valid=uv[:,:,0]>=0;dark=valid&(uv[:,:,2]<30)
  rows.append(dict(frame=i,side=side,capPixels=int(valid.sum()),darkPixels=int(dark.sum()),darkSourceCoordinates=np.unique(uv[dark,:2].astype(int),axis=0).tolist()))
(R/'uv-trace.json').write_text(json.dumps(rows,indent=2)+'\n');print(rows)
