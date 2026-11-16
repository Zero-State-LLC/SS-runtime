"""Metadata-only binding repair. Never render or rewrite an image."""
import replay
P=replay.HERE
out=P/'output'
before={str(p.relative_to(out)):replay.sha(p) for p in out.rglob('*.png')}
reg=replay.load(out/'registration.json')
replay.add_ground_boundary(reg)
replay.dump(out/'registration.json',reg)
manifest=replay.load(out/'manifest.json')
manifest['inputs']['replay.py']=replay.sha(P/'replay.py')
manifest['outputs']['registration.json']=replay.sha(out/'registration.json')
replay.dump(out/'manifest.json',manifest)
after={str(p.relative_to(out)):replay.sha(p) for p in out.rglob('*.png')}
assert before==after
result={'status':'PASS','allPNGBytesUnchanged':before,'registrationSHA256':replay.sha(out/'registration.json'),'manifestSHA256':replay.sha(out/'manifest.json'),'groundPixelsTopLeft':reg['groundPixelsTopLeft']}
replay.dump(P/'ground-binding-metadata-audit.json',result)
print(result)
