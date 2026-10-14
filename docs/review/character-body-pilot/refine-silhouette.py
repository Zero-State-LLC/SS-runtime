import bpy,math
from mathutils import Vector
scene=bpy.context.scene;scene.frame_set(1);rig=bpy.data.objects['SourceRig'];collection=bpy.data.collections['HERO_hooded_body']
# Replace the oval helmet-like opening with a tapered cloth hood contour.
contour=[(-.10,1.48),(-.15,1.59),(-.155,1.71),(-.105,1.82),(-.035,1.89),(0,1.90),(.035,1.89),(.105,1.82),(.155,1.71),(.15,1.59),(.10,1.48),(0,1.45)]
verts=[];faces=[];n=len(contour)
for y,factor in [(-.17,1),(-.06,1.06),(.07,.86),(.16,.4)]:
 for x,z in contour:verts.append((x*factor,y,1.67+(z-1.67)*factor))
for j in range(3):
 for i in range(n):faces.append((j*n+i,j*n+(i+1)%n,(j+1)*n+(i+1)%n,(j+1)*n+i))
faces.append(tuple(3*n+i for i in range(n)))
def replace_mesh(o,vs,fs):
 old=o.data;mesh=bpy.data.meshes.new(o.name+'_shape');mesh.from_pydata(vs,[],fs);mesh.update()
 for m in old.materials:mesh.materials.append(m)
 o.data=mesh;o.vertex_groups.clear();g=o.vertex_groups.new(name='head');g.add(list(range(len(vs))),1,'REPLACE')
 for p in mesh.polygons:p.use_smooth=True
replace_mesh(bpy.data.objects['HERO_hood'],verts,faces)
trim=[]
for f in [1,1.035]:
 for x,z in contour:trim.append((x*f,-.177,1.67+(z-1.67)*f))
replace_mesh(bpy.data.objects['HERO_hood_trim'],trim,[(i,(i+1)%n,n+(i+1)%n,n+i) for i in range(n)])
# Shadow inset conforms to cloth opening; avoid a separate oval face bulge.
shadow=bpy.data.objects['HERO_face_shadow'];shadow.location=(0,0,0);shadow.scale=(1,1,1)
replace_mesh(shadow,[(x*.86,-.16,1.67+(z-1.67)*.86) for x,z in contour],[tuple(range(n))])
# Replace segmented arm masses with continuous sleeves weighted across the elbow.
for side in ['L','R']:
 upper=rig.data.bones['upperArm.'+side];lower=rig.data.bones['forearm.'+side]
 a=upper.head_local.copy();b=upper.tail_local.copy();c=lower.tail_local.copy()
 stations=[(a+(b-a)*t,r,0) for t,r in [(0,.095),(.22,.09),(.65,.083),(1,.075)]]+[(b+(c-b)*t,r,t) for t,r in [(.3,.073),(.7,.064),(1,.06)]]
 vs=[];fs=[];rings=24
 for idx,(point,r,t) in enumerate(stations):
  tangent=(b-a) if idx<3 else (c-a if idx==3 else c-b)
  tangent.normalize();u=tangent.cross(Vector((0,1,0))).normalized();v=tangent.cross(u).normalized()
  for k in range(rings):
   angle=2*math.pi*k/rings;vs.append(tuple(point+r*(math.cos(angle)*u+math.sin(angle)*v)))
 for j in range(len(stations)-1):
  for k in range(rings):fs.append((j*rings+k,j*rings+(k+1)%rings,(j+1)*rings+(k+1)%rings,(j+1)*rings+k))
 m=bpy.data.meshes.new('Sleeve_'+side);m.from_pydata(vs,[],fs);m.update();m.materials.append(bpy.data.materials['MAT_charcoal_coat'])
 o=bpy.data.objects.new('HERO_sleeve_'+side,m);collection.objects.link(o);o.parent=rig
 gu=o.vertex_groups.new(name='upperArm.'+side);gl=o.vertex_groups.new(name='forearm.'+side)
 for j in range(len(stations)):
  t=0 if j<3 else .5 if j==3 else 1
  ids=list(range(j*rings,(j+1)*rings));gu.add(ids,1-t,'REPLACE');gl.add(ids,t,'REPLACE')
 arm=o.modifiers.new('EditableRigBinding','ARMATURE');arm.object=rig
 solid=o.modifiers.new('SleeveThickness','SOLIDIFY');solid.thickness=.006
 for p in m.polygons:p.use_smooth=True
 for prefix in ['HERO_upperArm_','HERO_forearm_']:bpy.data.objects.remove(bpy.data.objects[prefix+side],do_unlink=True)
scene.view_settings.exposure=.7
bpy.context.view_layer.update()
result={'revisionPurpose':'hood contour and continuous sleeve silhouette correction','bodyObjects':len(collection.objects),'hoodDimensions':list(bpy.data.objects['HERO_hood'].dimensions),'exposure':scene.view_settings.exposure,'sourceStatus':'pending silhouette review; not admitted'}
