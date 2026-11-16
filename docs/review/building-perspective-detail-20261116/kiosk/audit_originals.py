"""Read-only original-byte witness against tracked HEAD, with packet-local output."""
import hashlib, json, subprocess
from pathlib import Path
P=Path(__file__).resolve().parent
ROOT=P.parents[3]
PREFIX='docs/review/stone-painted-facade-20261116/'
SCREEN='docs/review/scene-qa-framing-20261116/native-capture-v6/source-scene-candidate-ordinary-z100-native.png'
paths=subprocess.check_output(['git','ls-files',PREFIX,SCREEN],cwd=ROOT,text=True).splitlines()
assert paths and SCREEN in paths
rows={}
for name in paths:
    expected=subprocess.check_output(['git','show','HEAD:'+name],cwd=ROOT)
    actual=(ROOT/name).read_bytes()
    assert actual==expected, 'Original byte mismatch: '+name
    rows[name]=hashlib.sha256(actual).hexdigest()
record={'status':'PASS','method':'Every tracked original stone packet file and the actual v6 screenshot byte-compared with HEAD','head':subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),'fileCount':len(rows),'sha256':rows}
(P/'original-byte-audit.json').write_text(json.dumps(record,indent=2)+'\n')
print(json.dumps({'status':'PASS','fileCount':len(rows),'head':record['head']}))
