# BP-002 body silhouette pilot. Procedural editable source, not benchmark art admission.
import bpy, math
from mathutils import Vector
scene=bpy.context.scene;scene.frame_set(1)
rig=bpy.data.objects['SourceRig']
collection=bpy.data.collections.new('HERO_hooded_body');scene.collection.children.link(collection)
def put(o):
 for c in list(o.users_collection):c.objects.unlink(o)
 collection.objects.link(o)
def material(name,color,roughness=.85):
 m=bpy.data.materials.new(name);m.diffuse_color=(*color,1);m.use_nodes=True
 bsdf=m.node_tree.nodes.get('Principled BSDF');bsdf.inputs['Base Color'].default_value=(*color,1);bsdf.inputs['Roughness'].default_value=roughness
 return m
cloth=material('MAT_charcoal_coat',(.065,.071,.078));pants=material('MAT_trousers',(.035,.041,.047));leather=material('MAT_dark_leather',(.025,.028,.03));trim=material('MAT_muted_tan',(.32,.27,.19));void=material('MAT_hood_shadow',(.008,.009,.01));sole=material('MAT_boot_sole',(.013,.014,.015))
def bind(o,bone):
 group=o.vertex_groups.new(name=bone);group.add(list(range(len(o.data.vertices))),1,'REPLACE')
 mod=o.modifiers.new('EditableRigBinding','ARMATURE');mod.object=rig
 o['source_role']='silhouette prototype; not admitted';o['bound_bone']=bone
 return o
def mesh(name,verts,faces,mat,bone):
 m=bpy.data.meshes.new(name);m.from_pydata(verts,[],faces);m.update();o=bpy.data.objects.new(name,m);collection.objects.link(o);m.materials.append(mat)
 for p in m.polygons:p.use_smooth=True
 bind(o,bone);return o
def ellipsoid(name,center,scale,mat,bone):
 bpy.ops.mesh.primitive_uv_sphere_add(segments=24,ring_count=12,radius=1,location=center)
 o=bpy.context.object;o.name=name;o.scale=scale
 bpy.ops.object.transform_apply(location=False,rotation=False,scale=True);put(o);o.data.materials.append(mat)
 for p in o.data.polygons:p.use_smooth=True
 return bind(o,bone)
def segment(name,a,b,radii,mat,bone):
 a=Vector(a);b=Vector(b);o=ellipsoid(name,(a+b)/2,(radii[0],radii[1],(b-a).length*.59),mat,bone)
 o.rotation_mode='QUATERNION';o.rotation_quaternion=(b-a).to_track_quat('Z','Y');return o
def ringmesh(name,rings,mat,bone,open_front=False):
 n=32;verts=[]
 for z,wx,wy,cy in rings:
  for i in range(n):
   angle=(-math.pi/2+.18+(2*math.pi-.36)*i/(n-1)) if open_front else 2*math.pi*i/n
   verts.append((wx*math.cos(angle),cy+wy*math.sin(angle),z))
 faces=[]
 for j in range(len(rings)-1):
  for i in range(n-1 if open_front else n):faces.append((j*n+i,j*n+(i+1)%n,(j+1)*n+(i+1)%n,(j+1)*n+i))
 if not open_front:faces += [tuple(reversed(range(n))),tuple((len(rings)-1)*n+i for i in range(n))]
 o=mesh(name,verts,faces,mat,bone)
 if open_front:
  s=o.modifiers.new('ClothThickness','SOLIDIFY');s.thickness=.009
 return o
# Underlayer and flared open-front coat, separate editable pieces.
ellipsoid('HERO_underlayer',(0,0,1.28),(.213,.135,.28),pants,'torso')
coat=ringmesh('HERO_coat',[(.72,.29,.18,0),(.84,.265,.16,0),(1.03,.205,.135,0),(1.15,.205,.135,0),(1.37,.25,.15,0),(1.48,.23,.13,0)],cloth,'torso',True)
# Lower coat follows pelvis, upper coat blends into torso; preserves editable weights.
coat.vertex_groups.clear();gp=coat.vertex_groups.new(name='pelvis');gt=coat.vertex_groups.new(name='torso')
for v in coat.data.vertices:
 t=max(0,min(1,(v.co.z-1.02)/.25));gp.add([v.index],1-t,'REPLACE');gt.add([v.index],t,'REPLACE')
ringmesh('HERO_belt',[(1.015,.214,.145,0),(1.055,.214,.145,0)],leather,'pelvis')
# Hood dome lofted from an open front rim to a closed rear, with thickness.
verts=[];faces=[];n=32
for y,rx,rz in [(-.17,.18,.22),(-.1,.20,.25),(0,.205,.25),(.10,.17,.21),(.18,.06,.08)]:
 for i in range(n):
  a=2*math.pi*i/n;verts.append((rx*math.cos(a),y,1.65+rz*math.sin(a)))
for j in range(4):
 for i in range(n):faces.append((j*n+i,j*n+(i+1)%n,(j+1)*n+(i+1)%n,(j+1)*n+i))
faces.append(tuple(4*n+i for i in range(n)))
hood=mesh('HERO_hood',verts,faces,cloth,'head');solid=hood.modifiers.new('HoodThickness','SOLIDIFY');solid.thickness=.012
ellipsoid('HERO_face_shadow',(0,-.155,1.63),(.145,.045,.185),void,'head')
ellipsoid('HERO_neck_wrap',(0,0,1.5),(.155,.14,.10),cloth,'torso')
# Narrow front hood trim as an editable mesh strip.
vs=[]
for radius in [1,1.035]:
 for i in range(n):
  a=2*math.pi*i/n;vs.append((radius*.18*math.cos(a),-.177,1.65+radius*.22*math.sin(a)))
mesh('HERO_hood_trim',vs,[(i,(i+1)%n,n+(i+1)%n,n+i) for i in range(n)],trim,'head')
for side,x in [('L',.14),('R',-.14)]:
 for role,mat,radii in [('thigh',pants,(.10,.105)),('shin',pants,(.083,.085)),('upperArm',cloth,(.085,.085)),('forearm',cloth,(.07,.075))]:
  b=rig.data.bones[role+'.'+side];segment('HERO_'+role+'_'+side,b.head_local,b.tail_local,radii,mat,role+'.'+side)
 b=rig.data.bones['forearm.'+side];end=b.tail_local
 ellipsoid('HERO_glove_'+side,end+Vector((0,-.012,-.035)),(.055,.06,.075),leather,'forearm.'+side)
 ellipsoid('HERO_thumb_'+side,end+Vector((-.035 if side=='L' else .035,-.037,-.015)),(.025,.03,.045),leather,'forearm.'+side)
 # Front knee pad stays with the shin in this first silhouette proof.
 k=rig.data.bones['shin.'+side].head_local
 ellipsoid('HERO_kneepad_'+side,k+Vector((0,-.08,-.045)),(.072,.025,.085),trim,'shin.'+side)
 # Foot shells are constructed around the rig ankle, with actual sole at source z=0.
 for role,rings,mat in [('boot',[(.035,.086,.17,-.075),(.07,.09,.17,-.075),(.13,.082,.145,-.055),(.22,.07,.075,0)],leather),('sole',[(0,.09,.175,-.075),(.035,.09,.175,-.075)],sole)]:
  o=ringmesh('HERO_'+role+'_'+side,rings,mat,'foot.'+side)
  for v in o.data.vertices:v.co.x+=x
# Asymmetric cross-body strap, front only at this blockout stage.
verts=[(-.17,-.154,1.08),(-.13,-.158,1.08),(.22,-.154,1.45),(.18,-.158,1.45)]
strap=mesh('HERO_front_strap',verts,[(0,1,2,3)],trim,'torso');s=strap.modifiers.new('StrapThickness','SOLIDIFY');s.thickness=.012
ellipsoid('HERO_left_arm_patch',(.31,-.064,1.36),(.04,.025,.065),trim,'upperArm.L')
ellipsoid('HERO_belt_buckle',(0,-.155,1.035),(.04,.015,.035),trim,'pelvis')
for o in bpy.data.objects:
 if o.name.startswith('DEBUG_bone_'):o.hide_render=True;o.hide_set(True)
scene.frame_set(1);bpy.context.view_layer.update()
result={'bodyObjects':len(collection.objects),'rig':rig.name,'sourceStatus':'silhouette blockout only; pending camera inspection','hoodDimensions':list(hood.dimensions),'coatDimensions':list(coat.dimensions),'noRuntimeChange':True}
