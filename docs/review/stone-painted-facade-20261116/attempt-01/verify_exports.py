"""Read actual OBJ/MTL exports back, mutate exported fields, and check real pixels."""
import argparse
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from PIL import Image
import replay
P=Path(__file__).resolve().parent

def read_obj(text):
    vertices=[]
    uvs=[]
    faces=[]
    group=None
    material=None
    for line in text.splitlines():
        fields=line.split()
        if not fields: continue
        if fields[0]=='v': vertices.append([float(v) for v in fields[1:]])
        elif fields[0]=='vt': uvs.append([float(fields[1]),1-float(fields[2])])
        elif fields[0]=='g': group=fields[1]
        elif fields[0]=='usemtl': material=fields[1]
        elif fields[0]=='f':
            pairs=[value.split('/') for value in fields[1:]]
            faces.append(dict(name=group,material=material,indices=[int(v[0])-1 for v in pairs],uv=[uvs[int(v[1])-1] for v in pairs]))
    return dict(vertices=vertices,faces=faces)

def read_mtl(text):
    textures={}
    name=None
    for line in text.splitlines():
        fields=line.split()
        if not fields: continue
        if fields[0]=='newmtl': name=fields[1]
        elif fields[0]=='map_Kd':
            path=(P/'output'/fields[1]).resolve()
            assert path.is_relative_to((P/'output').resolve()), 'Texture escaped export'
            with Image.open(path) as image: textures[name]=image.convert('RGBA')
    assert set(textures)=={'facade','door','roof'}
    return textures

def check():
    obj=(P/'output/building.obj').read_text()
    mtl=(P/'output/building.mtl').read_text()
    mesh=read_obj(obj)
    textures=read_mtl(mtl)
    rendered=replay.render(mesh,textures)
    with Image.open(P/'output/preview-alpha.png') as expected:
        assert rendered.tobytes()==expected.tobytes(), 'OBJ/MTL roundtrip changed pixels'
    changed_uv=obj.replace('vt 0 0\n','vt 0.2 0\n',1)
    assert changed_uv!=obj
    uv_mesh=read_obj(changed_uv)
    uv_render=replay.render(uv_mesh,textures)
    assert uv_mesh['vertices']==mesh['vertices']
    assert uv_render.tobytes()!=rendered.tobytes(), 'Actual exported UV mutation was inert'
    assert uv_render.getchannel('A').tobytes()==rendered.getchannel('A').tobytes()
    changed_mtl=mtl.replace('map_Kd textures/facade.png','map_Kd textures/door.png')
    assert changed_mtl!=mtl
    material_render=replay.render(mesh,read_mtl(changed_mtl))
    assert material_render.tobytes()!=rendered.tobytes(), 'Actual exported MTL mutation was inert'
    changed_obj=obj.replace(' 132\n',' 144\n')
    assert changed_obj!=obj
    geometry_render=replay.render(read_obj(changed_obj),textures)
    assert geometry_render.size!=rendered.size, 'Actual OBJ vertex mutation was inert'
    result=dict(status='PASS',objRoundtrip='pixel-identical',uvMutation='pixels change, geometry and alpha unchanged',mtlMutation='material map changes actual pixels',objVertexMutation='height changes derived canvas',sourceCanvas=list(rendered.size),sourceRoot=replay.registration(mesh)['sourceRoot'],uniformScale=.2)
    print(json.dumps(result,indent=2))

def clean_copy():
    with tempfile.TemporaryDirectory(prefix='clean-all-tests-',dir=P) as directory:
        root=Path(directory)
        for name in ('author.py','replay.py','test_source.py','verify_exports.py','mesh.json','materials.json'):
            shutil.copyfile(P/name,root/name)
        for name in ('inputs','output'): shutil.copytree(P/name,root/name)
        for script in ('test_source.py','verify_exports.py'):
            result=subprocess.run([sys.executable,str(root/script)],cwd=root,capture_output=True,text=True)
            print('CLEAN COPY:',script,flush=True)
            print(result.stdout,flush=True)
            print(result.stderr,flush=True)
            if result.returncode: raise SystemExit(result.returncode)
        print('CLEAN COPY: all 13 source tests and actual OBJ/MTL mutation checks PASS')

if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--clean-copy',action='store_true')
    args=parser.parse_args()
    if args.clean_copy: clean_copy()
    else: check()
