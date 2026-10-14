# Refine existing approved costume elements, not a new character design.
import bpy, math
from mathutils import Vector
scene=bpy.context.scene
scene.frame_set(1)
rig=bpy.data.objects['SourceRig']
col=bpy.data.collections['HERO_hooded_body']
def weighted_mesh(name,vs,fs,mat,weights):
 m=bpy.data.meshes.new(name);m.from_pydata(vs,[],fs);m.update()
 o=bpy.data.objects.new(name,m);col.objects.link(o);o.parent=rig;m.materials.append(bpy.data.materials[mat])
 groups={}
 for i,w in enumerate(weights):
  for bone,amount in w.items():
   if bone not in groups:groups[bone]=o.vertex_groups.new(name=bone)
   groups[bone].add([i],amount,'REPLACE')
 for p in m.polygons:p.use_smooth=True
 a=o.modifiers.new('EditableRigBinding','ARMATURE');a.object=rig
 return o
def torso_weights(z):
 t=max(0,min(1,(z-1.02)/.25))
 return {'pelvis':1-t,'torso':t}
# Continuous trouser topology, with rings and blended knee weights.
for side in ['L','R']:
 thigh=rig.data.bones['thigh.'+side];shin=rig.data.bones['shin.'+side]
 a=thigh.head_local.copy();b=thigh.tail_local.copy();c=shin.tail_local.copy()
 stations=[(a+(b-a)*t,r,w) for t,r,w in [(0,.105,0),(.2,.11,0),(.48,.105,0),(.75,.092,.05),(.9,.082,.25),(1,.079,.5)]]
 stations += [(b+(c-b)*t,r,w) for t,r,w in [(.12,.08,.75),(.3,.085,1),(.55,.078,1),(.8,.065,1),(1,.061,1)]]
 vs=[];fs=[];ws=[];n=32
 for j,(p,r,w) in enumerate(stations):
  tangent=(b-a) if j<4 else ((c-a) if j<7 else (c-b))
  tangent.normalize();u=tangent.cross(Vector((0,1,0))).normalized();v=tangent.cross(u).normalized()
  for k in range(n):
   angle=2*math.pi*k/n
   # Broad seam-side cloth undulation; no independent capsule at the knee.
   radius=r*(1+.025*math.cos(4*angle))
   vs.append(tuple(p+radius*(math.cos(angle)*u+math.sin(angle)*v)))
   ws.append({'thigh.'+side:1-w,'shin.'+side:w})
 for j in range(len(stations)-1):
  for k in range(n):fs.append((j*n+k,j*n+(k+1)%n,(j+1)*n+(k+1)%n,(j+1)*n+k))
 fs.extend([tuple(reversed(range(n))),tuple((len(stations)-1)*n+k for k in range(n))])
 weighted_mesh('HERO_trousers_'+side,vs,fs,'MAT_trousers',ws)
 for old in ['HERO_thigh_'+side,'HERO_shin_'+side]:bpy.data.objects.remove(bpy.data.objects[old],do_unlink=True)
 # Retain practical reinforced knees, reduce toy-like protrusion and contrast.
 pad=bpy.data.objects['HERO_kneepad_'+side]
 pad.scale=(.94,.45,.92);pad.data.materials.clear();pad.data.materials.append(bpy.data.materials['MAT_dark_leather'])
# Replace coat with a shaped open front and multiple longitudinal drape stations.
rings=[(.72,.285,.175,.52),(.80,.277,.167,.48),(.90,.25,.155,.42),(1.02,.219,.145,.27),(1.10,.216,.147,.24),(1.23,.232,.16,.26),(1.36,.249,.163,.36),(1.46,.234,.143,.52)]
vs=[];fs=[];ws=[];n=48
for z,rx,ry,gap in rings:
 for k in range(n):
  angle=-math.pi/2+gap+(2*math.pi-2*gap)*k/(n-1)
  fold=.008*max(0,(1.1-z)/.38)*math.cos(8*angle)
  vs.append(((rx+fold)*math.cos(angle),(ry+fold)*math.sin(angle),z))
  ws.append(torso_weights(z))
for j in range(len(rings)-1):
 for k in range(n-1):fs.append((j*n+k,j*n+k+1,(j+1)*n+k+1,(j+1)*n+k))
bpy.data.objects.remove(bpy.data.objects['HERO_coat'],do_unlink=True)
coat=weighted_mesh('HERO_coat',vs,fs,'MAT_charcoal_coat',ws)
solid=coat.modifiers.new('ClothThickness','SOLIDIFY');solid.thickness=.009
# Rolled open-front edges are continuous along the coat, including lower tails.
for edge,label in [(0,'R'),(n-1,'L')]:
 points=[Vector(vs[j*n+edge]) for j in range(len(rings))]
 ev=[];ef=[];ew=[];sides=8
 for j,p in enumerate(points):
  tangent=(points[min(j+1,len(points)-1)]-points[max(j-1,0)]).normalized()
  u=tangent.cross(Vector((0,1,0))).normalized();v=tangent.cross(u)
  for k in range(sides):
   q=p+.004*(math.cos(2*math.pi*k/sides)*u+math.sin(2*math.pi*k/sides)*v)
   ev.append(tuple(q));ew.append(torso_weights(p.z))
 for j in range(len(points)-1):
  for k in range(sides):ef.append((j*sides+k,j*sides+(k+1)%sides,(j+1)*sides+(k+1)%sides,(j+1)*sides+k))
 weighted_mesh('HERO_coat_edge_'+label,ev,ef,'MAT_dark_leather',ew)
# One physical strap loop across front, over shoulder, down back and around hip.
points=[]
for back in [False,True]:
 for i in range(17):
  t=i/16 if not back else 1-i/16
  x=-.18+.37*t;z=1.07+.40*t
  rx=.225+.02*t;ry=.156+.007*t
  y=math.sqrt(max(.001,1-(x/rx)**2))*ry+.009
  points.append(Vector((x,y if back else -y,z)))
# Add outer hip point to wrap the lower endpoints.
points.append(Vector((-.237,0,1.07)))
sv=[];sf=[];sw=[]
for j,p in enumerate(points):
 tangent=(points[(j+1)%len(points)]-points[(j-1)%len(points)]).normalized()
 normal=Vector((p.x/.23,p.y/.16,0)).normalized()
 across=tangent.cross(normal).normalized()*.016
 for q in [p-across,p+across]:sv.append(tuple(q));sw.append(torso_weights(p.z))
for j in range(len(points)):
 k=(j+1)%len(points);sf.append((2*j,2*j+1,2*k+1,2*k))
bpy.data.objects.remove(bpy.data.objects['HERO_front_strap'],do_unlink=True)
strap=weighted_mesh('HERO_crossbody_strap',sv,sf,'MAT_muted_tan',sw)
solid=strap.modifiers.new('StrapThickness','SOLIDIFY');solid.thickness=.005
scene.frame_set(1);bpy.context.view_layer.update()
result={'bodyObjects':len(col.objects),'changes':['continuous weighted trousers','flatter dark knee reinforcement','shaped coat opening and rolled edges','continuous front/shoulder/back/hip strap'],'sourceStatus':'pending multi-view review; not admitted'}
