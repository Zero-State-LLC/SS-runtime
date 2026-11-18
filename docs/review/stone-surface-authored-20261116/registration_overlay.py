"""Authored contact/collision overlay, never inferred from sprite alpha."""
from PIL import Image,ImageDraw
from replay import HERE,load,project
m=load(HERE/'model.json')
r=load(HERE/'registration.json')
with Image.open(HERE/'preview-alpha.png') as source:
    im=source.copy()
d=ImageDraw.Draw(im)
rectangle=[[0,0,0],[128,0,0],[128,128,0],[0,128,0],[0,0,0]]
d.line([project(v,m) for v in rectangle],fill='#e7b36e',width=3)
for mark in r['landmarks']:
    x,y=project(mark['local'],m)
    d.ellipse((x-4,y-4,x+4,y+4),fill='#5de3dc')
    text=mark['id']+(' virtual collision corner' if mark['id']=='A' else ' authored base')
    if mark['id']=='C':text+=' / hidden'
    d.text((max(5,min(x+6,910)),y+6),text,fill='#5de3dc')
im.save(HERE/'registration-overlay.png')
