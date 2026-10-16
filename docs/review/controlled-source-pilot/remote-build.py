"""BP-002 source scaffold, NOT character art. Run with Blender --background --python."""
import bpy,json,hashlib
from mathutils import Vector
bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
arm=bpy.data.armatures.new('SS_Hooded_Source_Scaffold');obj=bpy.data.objects.new('SourceRig',arm)
bpy.context.collection.objects.link(obj);bpy.context.view_layer.objects.active=obj;obj.select_set(True)
bpy.ops.object.mode_set(mode='EDIT')
def bone(name,head,tail,parent=None):
 b=arm.edit_bones.new(name);b.head=head;b.tail=tail
 if parent:b.parent=arm.edit_bones[parent]
 return b
bone('pelvis',(0,0,1),(0,0,1.15));bone('torso',(0,0,1.15),(0,0,1.55),'pelvis');bone('head',(0,0,1.55),(0,0,1.8),'torso')
for side,x in [('L',.14),('R',-.14)]:
 bone('thigh.'+side,(x,0,1),(x,-.1,.57),'pelvis')
 bone('shin.'+side,(x,-.1,.57),(x,0,.12),'thigh.'+side)
 bone('footTarget.'+side,(x,0,.12),(x,-.2,.12))
 bone('foot.'+side,(x,0,.12),(x,-.2,.12),'shin.'+side)
 bone('upperArm.'+side,(x*1.7,0,1.48),(x*2.3,-.02,1.18),'torso')
 bone('forearm.'+side,(x*2.3,-.02,1.18),(x*2.6,-.1,.96),'upperArm.'+side)
bpy.ops.object.mode_set(mode='POSE')
for side in ['L','R']:
 shin=obj.pose.bones['shin.'+side];ik=shin.constraints.new('IK');ik.name='FixedFootNoStretch';ik.target=obj;ik.subtarget='footTarget.'+side;ik.chain_count=2;ik.use_stretch=False
 for key in ['thigh.','shin.']:obj.pose.bones[key+side].ik_stretch=0
 foot=obj.pose.bones['foot.'+side];copy=foot.constraints.new('COPY_ROTATION');copy.target=obj;copy.subtarget='footTarget.'+side;copy.target_space='WORLD';copy.owner_space='WORLD'
# Translation in the pelvis bone's local axes is deliberately modest and reachable.
pelvis=obj.pose.bones['pelvis'];torso=obj.pose.bones['torso'];torso.rotation_mode='XYZ'
for frame,compression,lean in [(1,0,0),(4,-.055,.07),(7,0,0)]:
 pelvis.location=(0,compression,0);pelvis.keyframe_insert('location',frame=frame)
 torso.rotation_euler=(lean,0,0);torso.keyframe_insert('rotation_euler',frame=frame)
bpy.ops.object.mode_set(mode='OBJECT')
scene=bpy.context.scene;scene.frame_start=1;scene.frame_end=7;scene.render.fps=60
obj.show_in_front=True;arm.display_type='STICK'
# Technical camera only: fixed preview convention, not a selected production viewpoint.
bpy.ops.object.camera_add(location=(3,-4,4));camera=bpy.context.object
camera.rotation_euler=(Vector((0,0,.9))-camera.location).to_track_quat('-Z','Y').to_euler();camera.data.type='ORTHO';camera.data.ortho_scale=2.4;scene.camera=camera
rows=[]
for frame in range(1,8):
 scene.frame_set(frame);bpy.context.view_layer.update();evaluated=obj.evaluated_get(bpy.context.evaluated_depsgraph_get())
 values={}
 for side in ['L','R']:
  thigh=evaluated.pose.bones['thigh.'+side];shin=evaluated.pose.bones['shin.'+side];target=evaluated.pose.bones['footTarget.'+side]
  values[side]={'thighLength':float((thigh.tail-thigh.head).length),'shinLength':float((shin.tail-shin.head).length),'hip':list(thigh.head),'knee':list(shin.head),'ankle':list(shin.tail),'target':list(target.head),'targetResidual':float((shin.tail-target.head).length)}
 rows.append({'frame':frame,'legs':values})
scene.frame_set(1)

# Visible technical bone proxies: explicitly not body/costume geometry.
for name in [b.name for b in arm.bones if not b.name.startswith('footTarget')]:
    bpy.ops.mesh.primitive_uv_sphere_add(segments=12,ring_count=6,radius=1)
    proxy=bpy.context.object
    proxy.name='DEBUG_bone_'+name
    for frame in range(1,8):
        scene.frame_set(frame);bpy.context.view_layer.update()
        b=obj.evaluated_get(bpy.context.evaluated_depsgraph_get()).pose.bones[name]
        a=b.head.copy();z=b.tail.copy();direction=z-a
        proxy.location=(a+z)/2
        proxy.rotation_mode='QUATERNION';proxy.rotation_quaternion=direction.to_track_quat('Z','Y')
        proxy.scale=(.025,.025,direction.length/2)
        proxy.keyframe_insert('location',frame=frame);proxy.keyframe_insert('rotation_quaternion',frame=frame);proxy.keyframe_insert('scale',frame=frame)
scene.frame_set(1)
camera.name='CAM_technical'
for name,kind,location,energy in [('LGT_key','SUN',(2,-3,4),2),('LGT_fill','POINT',(-2,-2,2),80)]:
    data=bpy.data.lights.new(name,kind);data.energy=energy
    light=bpy.data.objects.new(name,data);bpy.context.collection.objects.link(light);light.location=location
    light.rotation_euler=(Vector((0,0,1))-light.location).to_track_quat('-Z','Y').to_euler()
scene.world=bpy.data.worlds.new('World') if scene.world is None else scene.world
scene.world.color=(.08,.08,.08)
scene.render.engine='BLENDER_EEVEE';scene.render.resolution_x=512;scene.render.resolution_y=512;scene.render.resolution_percentage=100
result={'status':'technical rig only, no costume or accepted art','samples':rows,'maxTargetResidual':max(v['targetResidual'] for r in rows for v in r['legs'].values()),'bones':len(arm.bones),'cameraType':camera.data.type}

