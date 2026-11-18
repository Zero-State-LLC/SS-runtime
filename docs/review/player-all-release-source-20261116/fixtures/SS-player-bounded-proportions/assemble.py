"""Whole-character source integration. Authored motion controls, not admitted animation."""
from pathlib import Path
import json,math,hashlib
import numpy as np
from PIL import Image,ImageDraw,ImageFilter
from thigh import render_thigh
R=Path(__file__).resolve().parent;S=R/'source';SIZE=(384,416)
rig=json.loads((S/'body-rig.json').read_text());poses=json.loads((S/'samples.json').read_text())
layers={p.stem:Image.open(p).convert('RGBA') for p in (S/'body-source').glob('*.png')}
def project(p):return np.array([192+6*p[0],336+6*(.5*p[1]-math.sqrt(.75)*p[2])])
def warp(im,A,b):
 inv=np.linalg.inv(A);off=-inv@b
 return im.transform(SIZE,Image.Transform.AFFINE,(*inv[0],off[0],*inv[1],off[1]),Image.Resampling.BICUBIC)
def bone(im,src_a,src_b,dst_a,dst_b):
 a=np.array(src_a);old=np.array(src_b)-a;new=dst_b-dst_a
 # Explicit projected depth deformation: preserve width, change projected axis length.
 axis=old/np.linalg.norm(old);normal=np.array([-axis[1],axis[0]])
 newaxis=new/np.linalg.norm(new);newnormal=np.array([-newaxis[1],newaxis[0]])
 A=np.outer(new,axis)/np.linalg.norm(old)+np.outer(newnormal,normal)
 return warp(im,A,dst_a-A@a)
def rotation(degrees):
 a=math.radians(degrees);return np.array([[math.cos(a),-math.sin(a)],[math.sin(a),math.cos(a)]])
def hem(im,dx,bob):
 # Preserve attachment rows; bend only the existing authored coat-tail region.
 a=np.array(im);out=Image.new('RGBA',SIZE)
 for y in range(a.shape[0]):
  w=max(0,min(1,(y-210)/48));x=round(dx*w*w);out.alpha_composite(im.crop((0,y,384,y+1)),(x,round(y+bob)))
 return out
def forearm(im,elbow,elbow_dst,hand_dst):
 # Deform sleeve to wrist; translate the glove rigidly so fingers do not stretch.
 wrist_y=182.; delta=hand_dst[1]-(elbow[1]+48)
 dst_wrist=wrist_y+delta; scale=(dst_wrist-elbow_dst[1])/(wrist_y-elbow[1])
 upper=im.transform(SIZE,Image.Transform.AFFINE,(1,0,0,0,1/scale,elbow[1]-elbow_dst[1]/scale),Image.Resampling.BICUBIC)
 lower=warp(im,np.eye(2),np.array([0,delta]))
 a=np.array(upper); b=np.array(lower); yy=np.arange(416)[:,None,None]
 # Continuous boundary at wrist, with one-pixel blend to avoid raster zipper.
 blend=np.clip(yy-dst_wrist+.5,0,1)
 return Image.fromarray(np.rint(a*(1-blend)+b*blend).astype(np.uint8))
frames=[];metrics=[];(R/'frames').mkdir(exist_ok=True)
for index,pose in enumerate(poses):
 t=pose['time'];phase=math.tau*t/.5;by_side={q['side']:q for q in pose['legs']}
 bob=-(pose['legs'][0]['hip'][2]-25.6)*6*math.sqrt(.75)
 parts={};depth=[];lower_rgba=np.zeros((416,384,4),dtype=np.uint8);lower_depth=np.full((416,384),-np.inf)
 for side in ['left','right']:
  q=by_side[side];hip=rig['bones'][side+'_hip']['pivot'];knee=rig['bones'][side+'_knee']['pivot']
  boot=Image.open(R/'boot'/'frames'/f'{index:02d}-{side}.png').convert('RGBA')
  thigh,thigh_depth=render_thigh(q,layers[side+'_thigh'],hip,knee)
  boot_depth=np.load(R/'boot'/'frames'/f'{index:02d}-{side}-depth.npy')
  for layer,z in [(boot,boot_depth),(thigh,thigh_depth)]:
   pixels=np.array(layer);mask=(pixels[:,:,3]>0)&(z>lower_depth);lower_rgba[mask]=pixels[mask];lower_depth[mask]=z[mask]
  # Hidden hip and knee underpaint follows the same authored limb deformation.
  hidden=Image.new('RGBA',SIZE)
  for name in []: # hidden surface now authored by the thigh volume, not rotating planar patches
   hidden.alpha_composite(bone(layers[name],hip,knee,project(q['hip']),project(q['knee'])))
  limb=Image.alpha_composite(hidden,boot);limb.alpha_composite(thigh);parts[side]=limb
  depth.append((sum(q[k][1]*math.sqrt(.75)+q[k][2]*.5 for k in ['hip','knee','ankle'])/3,side))
 legacy=Image.new('RGBA',SIZE)
 for _,side in sorted(depth):legacy.alpha_composite(parts[side])
 changed=int(np.any(np.array(legacy)!=lower_rgba,axis=2).sum())
 # Short local coat contact shadow, clipped to existing lower-body alpha.
 shadow=Image.new('L',SIZE)
 for name in ['left_coat_tail','right_coat_tail']:
  tail=hem(layers[name],4*math.sin(phase-math.pi/4)*(1 if name.startswith('right') else -1),bob)
  shadow=Image.fromarray(np.maximum(np.array(shadow),np.array(tail.getchannel('A'))))
 shadow=shadow.filter(ImageFilter.GaussianBlur(2.0))
 sh=np.zeros((416,384));sh[3:]=np.array(shadow)[:-3]/255
 lower_rgba[:,:,:3]=(lower_rgba[:,:,:3]*(1-.22*sh[:,:,None])).astype(np.uint8)
 out=Image.fromarray(lower_rgba)
 # Paint torso/coat/equipment from retained layers; do not re-generate identity.
 for name in ['torso_coat_equipment','left_coat_tail','right_coat_tail']:
  im=layers[name]
  if 'tail' in name:im=hem(im,4*math.sin(phase-math.pi/4)*(1 if name.startswith('right') else -1),bob)
  else:im=warp(im,np.eye(2),np.array([0,bob]))
  out.alpha_composite(im)
 # Restrained counter-swing uses existing editable shoulder/elbow layers and hidden overlaps.
 for side,sign in [('left',1),('right',-1)]:
  shoulder=np.array(rig['bones'][side+'_shoulder']['pivot']);elbow=np.array(rig['bones'][side+'_elbow']['pivot'])
  swing=sign*math.cos(phase)
  shoulder_dst=shoulder+np.array([0,bob])
  elbow_dst=elbow+np.array([0,bob+4*swing])
  hand=elbow+np.array([0,48])
  hand_dst=hand+np.array([0,bob+10*swing])
  for name in [side+'_shoulder_hidden',side+'_upper_arm']:
   out.alpha_composite(bone(layers[name],shoulder,elbow,shoulder_dst,elbow_dst))
  for name in [side+'_elbow_hidden',side+'_forearm_hand']:
   out.alpha_composite(forearm(layers[name],elbow,elbow_dst,hand_dst))
 out.alpha_composite(warp(layers['hood'],np.eye(2),np.array([0,bob])))
 out.save(R/'frames'/f'{index:02d}.png');bg=Image.new('RGB',SIZE,'#283036');bg.paste(out,(0,0),out);frames.append(bg)
 metrics.append({'frame':index,'time':t,'bodyBobPixels':bob,'pixelsDifferentFromAverageLayerSort':changed,'finiteDepthPixels':int(np.isfinite(lower_depth).sum()),'limbBackToFront':[side for _,side in sorted(depth)],'rgbaSHA256':hashlib.sha256(out.tobytes()).hexdigest()})
assert len(set(x['rgbaSHA256'] for x in metrics))==16
frames[0].save(R/'slow-character-cycle.gif',save_all=True,append_images=frames[1:],duration=125,loop=0)
sheet=Image.new('RGB',(1536,1792),'#283036');d=ImageDraw.Draw(sheet)
for i,im in enumerate(frames):
 x=i%4*384;y=i//4*448;sheet.paste(im,(x,y+32));d.text((x+12,y+10),f'{i+1:02d} | {poses[i]["time"]:.5f}s',fill='white')
sheet.save(R/'sixteen-character-poses.png')
(R/'assembly-record.json').write_text(json.dumps({'status':'WHOLE_CHARACTER_SOURCE_CANDIDATE_NOT_ADMITTED','cycleSeconds':.5,'previewFrameMilliseconds':125,'controls':{'projectedElbowSwingPixels':4,'projectedHandSwingPixels':10,'armPhase':'opposite-side cosine','coatHemPixels':4,'bodyBob':'derived from authored pelvis height'},'controlAuthority':'Authored candidate values, not research-derived acceptance criteria','depthPolicy':'shared per-pixel source depth for both boots/calves/thighs; coat and torso retain front-layer policy','limits':['Thigh plus authored anterior knee-cover surface; rear cloth is provisional','Torso/coat are still layered rather than part of the lower-body depth buffer','Material polish remains a proposed source finish','One facing only','No real-renderer world-travel test'] ,'frames':metrics},indent=2)+'\n')
print('16 distinct whole-character source poses exported.')
