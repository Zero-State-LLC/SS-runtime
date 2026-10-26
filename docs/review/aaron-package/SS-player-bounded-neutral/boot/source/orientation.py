"""Authored surface ownership study. No generated paint, runtime admission or anatomy measurement."""
from pathlib import Path
import json, math
import numpy as np
from PIL import Image, ImageDraw
import boot_geometry as b
R=Path(__file__).resolve().parent
verts=list(b.vertices); faces=list(b.faces); colors=list(b.colors)
groups=list(b.face_groups)
assert len(groups)==len(faces)
def quad(points,color,group):
 start=len(verts);verts.extend(points);faces.append(list(range(start,start+4)));colors.append(color);groups.append(group)
def top(y):
 ss=b.P['sections']
 for (a,wa,ha),(c,wc,hc) in zip(ss,ss[1:]):
  if a<=y<=c:return ha+(hc-ha)*(y-a)/(c-a)
 raise ValueError(y)
# Tongue over upper instep; negative local Y is heel, zero is toe.
for y0,y1 in [(-6,-5),(-5,-4),(-4,-3)]:
 quad([b.point(x,y,top(y)+.025) for x,y in [(-.8,y0),(.8,y0),(.8,y1),(-.8,y1)]],(60,46,33),'tongue_instep')
# Cross-laces are small ribbons on that surface, never painted onto side/back/sole.
for y0 in [-5.8,-5,-4.2]:
 for sign in [-1,1]:
  pts=[]
  for x,y in [(-.75*sign,y0),(.75*sign,y0+.65),(.75*sign,y0+.74),(-.75*sign,y0+.09)]:
   pts.append(b.point(x,y,top(y)+.065))
  quad(pts,(168,148,112),'laces_instep')
# The shaft's forward surface is the foot-forward vector projected perpendicular to shin.
f=np.array(b.point(0,1,0))-np.array(b.point(0,0,0));axis=np.array(b.axis)
f=f-axis*np.dot(f,axis);f=f/np.linalg.norm(f)
lateral=np.cross(axis,f);lateral=lateral/np.linalg.norm(lateral)
def shaft(s,x,offset=1.83):return tuple(np.array(b.leg['ankle'])+axis*s+f*offset+lateral*x)
quad([shaft(s,x) for s,x in [(0,-.65),(0,.65),(3.45,.65),(3.45,-.65)]],(60,46,33),'tongue_shaft_front')
for s in [.3,1.3,2.3]:
 for sign in [-1,1]:
  quad([shaft(t,x,1.87) for t,x in [(s,-.6*sign),(s+.7,.6*sign),(s+.8,.6*sign),(s+.1,-.6*sign)]],(168,148,112),'laces_shaft_front')
# Source checks concern ownership only. Geometry is not benchmark art.
assert all('laces' not in g for g in groups[:70])
assert np.dot(f,np.array(b.point(0,1,0))-np.array(b.point(0,0,0)))>0
with (R/'recovery-leg-owned.obj').open('w') as out:
 out.write('# Authored surface ownership; lace ribbons are open overlay geometry\n')
 for p in verts:out.write('v '+' '.join(map(str,p))+'\n')
 for g,face in zip(groups,faces):out.write('g '+g+'\nf '+' '.join(str(i+1) for i in face)+'\n')
# Orthographic depth-buffered rendering prevents rear laces showing through the boot.
def render(az,title,elevation=30,fullpose=False):
 size=420;rgb=np.zeros((size,size,3),dtype=np.uint8);rgb[:]=(37,43,47);depth=np.full((size,size),-np.inf)
 elev=math.radians(elevation);az=math.radians(az)
 right=np.array([math.cos(az),-math.sin(az),0]);toward=np.array([math.sin(az)*math.cos(elev),math.cos(az)*math.cos(elev),math.sin(elev)])
 up=np.cross(right,toward);center=np.array(b.leg['ankle'])+axis*2
 if fullpose:center=np.zeros(3)
 v=np.array(verts)-center
 scale=6 if fullpose else 15;ox=192 if fullpose else 210;oy=336 if fullpose else 240
 screen=np.c_[ox+v@right*scale,oy-v@up*scale,v@toward]
 for face,col in zip(faces,colors):
  for j in range(1,len(face)-1):
   ids=[face[0],face[j],face[j+1]];p=screen[ids];a,c,d=p
   lo=np.maximum(np.floor(p[:,:2].min(axis=0)).astype(int),0);hi=np.minimum(np.ceil(p[:,:2].max(axis=0)).astype(int),size-1)
   if np.any(lo>hi):continue
   yy,xx=np.mgrid[lo[1]:hi[1]+1,lo[0]:hi[0]+1];xx=xx+.5;yy=yy+.5
   den=(c[1]-d[1])*(a[0]-d[0])+(d[0]-c[0])*(a[1]-d[1])
   if abs(den)<1e-9:continue
   u=((c[1]-d[1])*(xx-d[0])+(d[0]-c[0])*(yy-d[1]))/den
   w=((d[1]-a[1])*(xx-d[0])+(a[0]-d[0])*(yy-d[1]))/den;t=1-u-w
   z=u*a[2]+w*c[2]+t*d[2];sl=np.s_[lo[1]:hi[1]+1,lo[0]:hi[0]+1]
   mask=(u>=0)&(w>=0)&(t>=0)&(z>depth[sl]);depth[sl][mask]=z[mask]
   raw=np.array(verts)[ids];n=np.cross(raw[1]-raw[0],raw[2]-raw[0]);n/=np.linalg.norm(n)
   light=.6+.4*abs(np.dot(n,np.array([-.2,.4,.8944])))
   rgb[sl][mask]=np.array(col)*light
 im=Image.fromarray(rgb)
 if fullpose:
  globals()['last_depth']=depth[:416,:384].copy()
  im=im.convert('RGBA');im.putalpha(Image.fromarray((np.isfinite(depth)*255).astype(np.uint8)));return im.crop((0,0,384,416))
 dr=ImageDraw.Draw(im);dr.text((12,12),title,fill='white');return im
plate=Image.new('RGB',(840,840))
views=[(0,30,'ELEVATED FRONT: SURFACE REVIEW'),(90,30,'RECOVERY: SIDE'),(180,30,'ELEVATED BACK / HEEL'),(0,-60,'UNDERSIDE DIAGNOSTIC: TONGUE / LACES')]
for i,(angle,elevation,title) in enumerate(views):plate.paste(render(angle,title,elevation),(420*(i%2),420*(i//2)))
plate.save(R/'orientation-review.png')
(R/'surface-ownership.json').write_text(json.dumps({'status':'SOURCE_STUDY_NOT_FINAL_ART','coordinateConvention':'local foot Y increases heel to toe; local Z is sole to upper','lacesAllowed':['tongue_instep','tongue_shaft_front'],'lacesForbidden':['heel_counter','back_shaft','outsole','lateral_quarter'],'faceGroups':groups,'shaftForward':f.tolist(),'research':'https://nicksboots.com/pages/glossary','dimensions':'Authored guide values; not inferred anatomy'},indent=2)+'\n')
print('Exported semantic mesh and four depth-buffered views; ownership assertions passed.')

# Full-character source placement uses the existing guide projection without fitting to paint.
original=Image.open(R/'retained-contact.png').convert('RGBA')
proxy=render(0,'',30,True);proxy.save(R/'fullpose-proxy.png')
assembled=Image.alpha_composite(proxy,original);assembled.save(R/'fullpose-behind.png')
plate=Image.new('RGB',(1152,448),'#283036');dr=ImageDraw.Draw(plate)
for i,(im,label) in enumerate([(original,'Retained painted contact'),(assembled,'Source behind retained paint'),(Image.alpha_composite(original,proxy),'Source overlay diagnostic')]):
 plate.paste(im,(384*i,32),im);dr.text((384*i+12,12),label,fill='white')
plate.save(R/'fullpose-comparison.png')
