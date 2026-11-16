"""Editable Catmull-Clark surface refinement, with authored sole-plane/end constraints."""
from collections import defaultdict
import numpy as np

def subdivide(vertices,faces,colors,groups,point,passes=2):
 v=np.array(vertices,dtype=float)
 # Foot-local inverse basis. Geometry is rigidly posed, so constraints stay local.
 origin=np.array(point(0,0,0));basis=np.array([np.array(point(*p))-origin for p in [(1,0,0),(0,1,0),(0,0,1)]])
 for _ in range(passes):
  fp=np.array([v[f].mean(axis=0) for f in faces]);edge_faces=defaultdict(list);vertex_faces=defaultdict(list);neighbors=defaultdict(set)
  for fi,f in enumerate(faces):
   for i,a in enumerate(f):
    b=f[(i+1)%len(f)];edge_faces[tuple(sorted((a,b)))].append(fi);vertex_faces[a].append(fi);neighbors[a].add(b);neighbors[b].add(a)
  assert all(len(fs)==2 for fs in edge_faces.values())
  new=[];original=[]
  for i,p in enumerate(v):
   fs=vertex_faces[i];n=len(fs);F=fp[fs].mean(axis=0);E=np.array([(p+v[j])/2 for j in neighbors[i]]).mean(axis=0)
   new.append((F+2*E+(n-3)*p)/n);original.append(p)
  edge_ids={}
  for (a,b),fs in edge_faces.items():
   edge_ids[a,b]=len(new);new.append((v[a]+v[b]+fp[fs[0]]+fp[fs[1]])/4);original.append((v[a]+v[b])/2)
  face_ids=[]
  for p in fp:face_ids.append(len(new));new.append(p);original.append(p)
  new=np.array(new);original=np.array(original)
  # Preserve the authored shoe's sole plane and end planes only for shoe-component vertices.
  shoefaces=[i for i,g in enumerate(groups) if g.startswith('boot_')]
  shoe=set()
  for fi in shoefaces:
   shoe.add(face_ids[fi]);f=faces[fi]
   for i,a in enumerate(f):shoe.add(a);shoe.add(edge_ids[tuple(sorted((a,f[(i+1)%len(f)])))])
  for i in shoe:
   old=(original[i]-origin)@basis.T;local=(new[i]-origin)@basis.T
   if abs(old[2])<1e-8:local[2]=0
   if abs(old[1])<1e-8:local[1]=0
   if abs(old[1]+10)<1e-8:local[1]=-10
   new[i]=origin+local@basis
  nf=[];nc=[];ng=[]
  for fi,f in enumerate(faces):
   for j,a in enumerate(f):
    nf.append([a,edge_ids[tuple(sorted((a,f[(j+1)%len(f)])))],face_ids[fi],edge_ids[tuple(sorted((f[j-1],a)))]])
    nc.append(colors[fi]);ng.append(groups[fi])
  v=new;faces=nf;colors=nc;groups=ng
 assert np.isfinite(v).all()
 return list(map(tuple,v)),faces,colors,groups
