"""Replay hand-edited mesh.json plus hand-painted surface PNGs without regeneration.
Example: python3 replay_painted.py --surfaces surfaces --out painted-replay.png
"""
import argparse
from pathlib import Path
from PIL import Image
from replay import HERE, load, render

parser=argparse.ArgumentParser()
parser.add_argument('--mesh',type=Path,default=HERE/'mesh.json')
parser.add_argument('--model',type=Path,default=HERE/'model.json')
parser.add_argument('--surfaces',type=Path,default=HERE/'surfaces')
parser.add_argument('--out',type=Path,default=HERE/'painted-direct-replay.png')
args=parser.parse_args()
mesh=load(args.mesh)
textures={}
for name in sorted({p['material'] for p in mesh}):
    with Image.open(args.surfaces/(name+'.png')) as im:
        if im.size!=(512,512):raise ValueError('Paint surface must be 512x512')
        textures[name]=im.convert('RGB')
render(load(args.model),mesh,textures).save(args.out)
print(args.out)
