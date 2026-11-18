"""Authored thigh surface: source paint belongs to the front; rear is plain cloth."""
import numpy as np,math,json
from pathlib import Path
MODEL=json.loads((Path(__file__).parent/'model.json').read_text())
from PIL import Image

def cloth_sample(texture, x, y, base=(63,61,55)):
 """Bilinear premultiplied source paint over complete authored cloth underpaint."""
 x=np.clip(x,0,texture.shape[1]-1);y=np.clip(y,0,texture.shape[0]-1)
 x0=np.floor(x).astype(int);y0=np.floor(y).astype(int)
 x1=np.minimum(x0+1,texture.shape[1]-1);y1=np.minimum(y0+1,texture.shape[0]-1)
 dx=(x-x0)[...,None];dy=(y-y0)[...,None]
 result=np.zeros((*x.shape,3),dtype=float)
 for sx,sy,weight in [(x0,y0,(1-dx)*(1-dy)),(x1,y0,dx*(1-dy)),(x0,y1,(1-dx)*dy),(x1,y1,dx*dy)]:
  sample=texture[sy,sx].astype(float);alpha=sample[...,3:4]/255
  result+=weight*(sample[...,:3]*alpha+np.array(base)*(1-alpha))
 return np.clip(np.rint(result),0,255).astype(np.uint8)

def render_thigh(pose,paint,hip_uv,knee_uv,size=(384,416)):
 h=np.array(pose['hip']);k=np.array(pose['knee']);axis=(k-h)/np.linalg.norm(k-h)
 # Lateral direction stays tied to the body. Forward follows the thigh surface.
 lateral=np.array([1.,0,0]);lateral-=axis*np.dot(lateral,axis);lateral/=np.linalg.norm(lateral)
 forward=np.cross(lateral,axis)
 vertices=[];uv=[];faces=[];front=[]
 garment_hip=h.copy();garment_hip[2]=MODEL['clothHipHeight']
 for (t,r),(_,uvr) in zip(MODEL['thighProfile'],MODEL['thighUVProfile']):
  c=garment_hip+(k-garment_hip)*t
  for j in range(16):
   a=j*math.tau/16;vertices.append(c+r*(lateral*math.sin(a)+forward*math.cos(a)))
   cloth_end=np.array([knee_uv[0],knee_uv[1]-20])
   center=np.array(hip_uv)+(cloth_end-hip_uv)*t
   uv.append((center[0]+uvr*6*math.sin(a),center[1]))
 for ring in range(4):
  for j in range(16):
   faces.append([ring*16+j,ring*16+(j+1)%16,(ring+1)*16+(j+1)%16,(ring+1)*16+j]);front.append(math.cos((j+.5)*math.tau/16)>0)
 # Author a joint cover around the bend; the pad belongs only to its anterior surface.
 ankle=np.array(pose['ankle']);chain=ankle-h;foot_on_chain=h+chain*np.dot(k-h,chain)/np.dot(chain,chain)
 anterior=k-foot_on_chain;anterior/=np.linalg.norm(anterior)
 across=np.array([1.,0,0]);across-=anterior*np.dot(across,anterior);across/=np.linalg.norm(across)
 up=np.cross(across,anterior);up/=np.linalg.norm(up)
 start=len(vertices);radius=MODEL['kneeCoverRadius']
 pad_center=k+anterior*MODEL['kneeCoverAnteriorOffset']
 depth_radius=MODEL['kneeCoverDepthRadius'];vertical_radius=MODEL['kneeCoverVerticalRadius']
 for row in range(13):
  latitude=-math.pi/2+row*math.pi/12
  for j in range(24):
   longitude=j*math.tau/24
   x=math.cos(latitude)*math.sin(longitude);y=math.sin(latitude);z=math.cos(latitude)*math.cos(longitude)
   vertices.append(pad_center+radius*across*x+vertical_radius*up*y+depth_radius*anterior*z)
   # Fixed neutral-view material projection, carried by the joint surface.
   # The original paint already contains the elevated-view foreshortening.
   uv.append((knee_uv[0]+10*x/.86,knee_uv[1]-16+14*((.5*z-math.sqrt(.75)*y)+.674)/1.674))
 for row in range(12):
  for j in range(24):
   faces.append([start+row*24+j,start+row*24+(j+1)%24,start+(row+1)*24+(j+1)%24,start+(row+1)*24+j])
   front.append(math.cos((j+.5)*math.tau/24)>0 )
 tex=np.array(paint);rgb=np.zeros((size[1],size[0],4),dtype=np.uint8);depth=np.full((size[1],size[0]),-np.inf)
 owner=np.zeros((size[1],size[0]),dtype=np.uint8)
 v=np.array(vertices);screen=np.c_[192+6*v[:,0],336+6*(.5*v[:,1]-math.sqrt(.75)*v[:,2]),v[:,1]*math.sqrt(.75)+v[:,2]*.5]
 for fi,f in enumerate(faces):
  for j in [1,2]:
   ids=[f[0],f[j],f[j+1]];p=screen[ids];a,b,c=p
   lo=np.maximum(np.floor(p[:,:2].min(axis=0)).astype(int),0);hi=np.minimum(np.ceil(p[:,:2].max(axis=0)).astype(int),[size[0]-1,size[1]-1])
   if np.any(lo>hi):continue
   yy,xx=np.mgrid[lo[1]:hi[1]+1,lo[0]:hi[0]+1];xx=xx+.5;yy=yy+.5
   den=(b[1]-c[1])*(a[0]-c[0])+(c[0]-b[0])*(a[1]-c[1])
   if abs(den)<1e-9:continue
   u=((b[1]-c[1])*(xx-c[0])+(c[0]-b[0])*(yy-c[1]))/den
   w=((c[1]-a[1])*(xx-c[0])+(a[0]-c[0])*(yy-c[1]))/den;t=1-u-w
   z=u*a[2]+w*b[2]+t*c[2];sl=np.s_[lo[1]:hi[1]+1,lo[0]:hi[0]+1];mask=(u>=0)&(w>=0)&(t>=0)&(z>depth[sl]);depth[sl][mask]=z[mask]
   color=np.zeros((*u.shape,4),dtype=np.uint8);color[:]=(63,61,55,255)
   if front[fi]:
    q=np.array(uv)[ids];sx=u*q[0,0]+w*q[1,0]+t*q[2,0];sy=u*q[0,1]+w*q[1,1]+t*q[2,1]
    color[:,:,:3]=cloth_sample(tex,sx,sy)
   if fi>=64:
    # Authored closed knee-pad cap; surface coordinates stay tied to knee axes.
    world=u[:,:,None]*v[ids[0]]+w[:,:,None]*v[ids[1]]+t[:,:,None]*v[ids[2]]
    rel=world-pad_center; px=rel@across/radius; py=rel@up/vertical_radius; pz=rel@anterior/depth_radius
    cap=(pz>.28)&(np.abs(px)<.86)&(np.abs(py)<.94)&((np.abs(px)+np.abs(py))<1.52)
    # Retain the sampled anterior paint instead of replacing it with procedural grain.
    # Retain sampled anterior paint; revised cover radius comes from model.json.
    # Rear cloth remains a separate surface material, not a mirrored front bitmap.
    color[:,:,:3]=np.where(cap[:,:,None],color[:,:,:3],np.array([52,51,47])).astype(np.uint8)
   rgb[sl][mask]=color[mask]
   owner[sl][mask]=2 if fi>=64 else 1
 # Diagnostic layers come from actual source face ownership and depth, not partitioning a flattened export.
 parts=Path(__file__).parent/'parts';parts.mkdir(exist_ok=True)
 for value,name in [(1,'thigh-cloth'),(2,'knee-cover')]:
  pixels=rgb.copy();pixels[owner!=value]=0
  Image.fromarray(pixels).save(parts/f'{pose["side"]}-{name}.png')
 return Image.fromarray(rgb),depth
