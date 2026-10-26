"""Authored connected boot source: open vamp patch lofted into shaft."""
from pathlib import Path
import math,json
import numpy as np
import block
from smooth import subdivide
R=Path(__file__).resolve().parent
P=json.loads((R/'boot-shape.json').read_text())
leg=json.loads((R/'authored-key.json').read_text());vertices=[];faces=[];colors=[];face_groups=[]
def add(v):vertices.append(tuple(v));return len(vertices)-1
def face(ids,color,group='boot_upper'):faces.append(ids);colors.append(color);face_groups.append(group)
def point(x,y,z):
 dy,dz=block.foot_rotation(y,z,leg['angle'])
 return (leg['toe'][0]+x,leg['toe'][1]+dy,leg['toe'][2]+dz)
def sub(a,b):return tuple(x-y for x,y in zip(a,b))
def norm(v):
 n=math.sqrt(sum(x*x for x in v));return tuple(x/n for x in v)
def cross(a,b):return (a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0])
calf_length=math.dist(leg['knee'],leg['ankle'])
axis=norm(sub(leg['knee'],leg['ankle']));axisn=np.array(axis)
forward=np.array(point(0,1,0))-np.array(point(0,0,0));forward-=axisn*np.dot(forward,axisn);forward/=np.linalg.norm(forward)
lateral=np.cross(forward,axisn);lateral/=np.linalg.norm(lateral)
rings=[]
for y,w,h in P['sections']:
 ring=[(-w*.65,0),(-w,.35),(-w*.95,h*.65),(-w*.55,h),(w*.55,h),(w*.95,h*.65),(w,.35),(w*.65,0)]
 rings.append([add(point(x,y,z)) for x,z in ring])
for i,(a,b) in enumerate(zip(rings,rings[1:])):
 for j in range(8):
  if i==1 and j in [2,3,4]:continue # single eight-edge opening in upper vamp
  face([a[j],a[(j+1)%8],b[(j+1)%8],b[j]],(103,79,49) if j!=7 else (40,35,29),'boot_upper' if j!=7 else 'boot_sole')
face(list(reversed(rings[0])),(70,54,35));face(rings[-1],(103,79,49))
# Opening winds around the removed top patch. Connect it to shaft rings, without an internal cap.
opening=[rings[1][j] for j in [2,3,4,5]]+[rings[2][j] for j in [5,4,3,2]]
angles=[-150,-120,-60,-30,30,60,120,150]
previous=opening
for dist,radius in [(.7,1.68),(2.6,1.80),(3.4,1.80),(3.6,1.80)]:
 center=np.array(leg['ankle'])+axisn*dist
 ring=[add(center+radius*(lateral*math.cos(math.radians(a))+forward*math.sin(math.radians(a)))) for a in angles]
 for j in range(8):face([previous[j],previous[(j+1)%8],ring[(j+1)%8],ring[j]],(105,82,52),'shaft')
 previous=ring
face(previous,(105,82,52),'shaft')
# Source topology: one boot component before refinement. Garment remains separate.
from collections import Counter
edges=Counter(tuple(sorted((f[i],f[(i+1)%len(f)]))) for f in faces for i in range(len(f)))
assert all(c==2 for c in edges.values())
boot_vertices_before=len(vertices);boot_faces_before=len(faces)
vertices,faces,colors,face_groups=subdivide(vertices,faces,colors,face_groups,point)
boot_vertex_count=len(vertices);boot_face_count=len(faces)
# Retain the garment tube; it overlaps the boot cuff and is not part of its topology.
u=norm(cross(axis,(1,0,0)));v=cross(axis,u);rr=[]
for dist,radius in [(3.45,1.86),(7,2.38),(11,2.55),(13.5,2.15)]:
 dist=3.45+(dist-3.45)*(calf_length-3.45)/(13.5-3.45)
 c=tuple(leg['ankle'][i]+axis[i]*dist for i in range(3))
 rr.append([add(tuple(c[i]+radius*(math.cos(j*math.tau/12)*u[i]+math.sin(j*math.tau/12)*v[i]) for i in range(3))) for j in range(12)])
for a,b in zip(rr,rr[1:]):
 for j in range(12):face([a[j],a[(j+1)%12],b[(j+1)%12],b[j]],(63,65,62),'trouser')
face(list(reversed(rr[0])),(63,65,62),'trouser');face(rr[-1],(63,65,62),'trouser')
# Kept as a source-extraction boundary for the existing material preview recipe.
with (R/'recovery-leg.obj').open('w') as out:
 for p in vertices:out.write('v '+' '.join(map(str,p))+'\n')
 for f in faces:out.write('f '+' '.join(str(i+1) for i in f)+'\n')
