import bpy,math
scene=bpy.context.scene
rig=bpy.data.objects['SourceRig']
scene.frame_set(1)
scene.render.resolution_x=384
scene.render.resolution_y=384
scene.render.resolution_percentage=100
scene.render.image_settings.media_type='IMAGE'
scene.render.image_settings.file_format='PNG'
for degrees in [0,180]:
 rig.rotation_euler.z=math.radians(degrees)
 bpy.context.view_layer.update()
 target=artifacts.file(name='costume-angle-'+str(degrees)+'.png',media_type='image/png')
 scene.render.filepath=str(target.path)
 bpy.ops.render.render(write_still=True)
 target.publish()
result={'angles':[0,180],'frame':1,'camera':scene.camera.name,'rotationConvention':'rig Z rotation; fixed camera and illumination','status':'source review only'}
