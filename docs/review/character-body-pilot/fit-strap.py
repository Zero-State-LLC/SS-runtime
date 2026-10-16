import bpy,math
from mathutils import Vector
from mathutils.bvhtree import BVHTree
scene=bpy.context.scene;scene.frame_set(1)
coat=bpy.data.objects['HERO_coat'];strap=bpy.data.objects['HERO_crossbody_strap'];rig=bpy.data.objects['SourceRig']
tree=BVHTree.FromPolygons([v.co.copy() for v in coat.data.vertices],[list(p.vertices) for p in coat.data.polygons])
old=strap.data
centers=[(old.vertices[i].co+old.vertices[i+1].co)*.5 for i in range(0,len(old.vertices),2)]
# Interpolate the closed loop before surface projection to remove abrupt hip corners.
samples=[]
for i,p1 in enumerate(centers):
 p0=centers[(i-1)%len(centers)];p2=centers[(i+1)%len(centers)];p3=centers[(i+2)%len(centers)]
 for k in range(4):
  t=k/4
  samples.append(.5*((2*p1)+(-p0+p2)*t+(2*p0-5*p1+4*p2-p3)*t*t+(-p0+3*p1-3*p2+p3)*t*t*t))
vs=[];fs=[];projected=0
for i,p in enumerate(samples):
 tangent=(samples[(i+1)%len(samples)]-samples[(i-1)%len(samples)]).normalized()
 outward=Vector((p.x/.23,p.y/.16,0)).normalized()
 across=tangent.cross(outward).normalized()*.016
 for q in [p-across,p+across]:
  radial=Vector((q.x,q.y,0)).normalized()
  origin=Vector((radial.x,radial.y,q.z))
  hit,normal,index,distance=tree.ray_cast(origin,-radial,2)
  if hit is not None:
   if normal.dot(radial)<0:normal=-normal
   q=hit+normal*.007;projected+=1
  vs.append(tuple(q))
for i in range(len(samples)):
 j=(i+1)%len(samples);fs.append((2*i,2*i+1,2*j+1,2*j))
m=bpy.data.meshes.new('HERO_crossbody_strap_surface_fit');m.from_pydata(vs,[],fs);m.update()
for mat in old.materials:m.materials.append(mat)
strap.data=m;strap.vertex_groups.clear();gp=strap.vertex_groups.new(name='pelvis');gt=strap.vertex_groups.new(name='torso')
for v in m.vertices:
 t=max(0,min(1,(v.co.z-1.02)/.25));gp.add([v.index],1-t,'REPLACE');gt.add([v.index],t,'REPLACE')
for p in m.polygons:p.use_smooth=True
bpy.context.view_layer.update()
result={'strapVertices':len(vs),'surfaceProjectedVertices':projected,'unprojectedVertices':len(vs)-projected,'unprojectedReason':'open front or shoulder beyond coat surface; requires visual review','sourceStatus':'not admitted'}
