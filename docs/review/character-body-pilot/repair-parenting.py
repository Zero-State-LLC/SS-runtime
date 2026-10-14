# Applied after the body build, on inspected revision 2; committed as revision 3.
rig=bpy.data.objects['SourceRig']
for o in bpy.data.collections['HERO_hooded_body'].objects:
    matrix=o.matrix_world.copy();o.parent=rig;o.matrix_world=matrix
for o in list(bpy.data.objects):
    if o.name.startswith('DEBUG_bone_'):
        bpy.data.objects.remove(o,do_unlink=True)
