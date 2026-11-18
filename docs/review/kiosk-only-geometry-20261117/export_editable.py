"""Export original indexed mesh plus Z-only candidate, preserving every face/UV."""
import copy
import json
from pathlib import Path
import build as b


def export(out):
    if out.exists():
        raise RuntimeError('Editable output exists, refusing overwrite')
    out.mkdir()
    source=b.a.OLD/'kiosk/output/mesh.json'
    original=json.loads(source.read_text())
    candidate=copy.deepcopy(original)
    mapping=dict(json.loads((b.HERE/'z-map.json').read_text())['anchors'])
    for vertex in candidate['vertices']:
        vertex[2]=mapping[vertex[2]]
    candidate['height']=mapping[original['height']]
    (out/'current-indexed-mesh.json').write_bytes(source.read_bytes())
    b.a.dump(out/'candidate-indexed-mesh.json',candidate)
    validate(original,candidate)
    (out/'DIMENSIONS.md').write_text(report())
    b.a.dump(out/'manifest.json',dict(sourcePath=str(source.relative_to(b.ROOT)),sourceSHA256=b.a.sha(source),zMapSHA256=b.a.sha(b.HERE/'z-map.json'),exporterSHA256=b.a.sha(Path(__file__)),comparisonManifestSHA256=b.a.sha(b.HERE/'output/manifest.json'),outputs={p.name:b.a.sha(p) for p in sorted(out.iterdir())},qualification='Editable UV correspondence retained, NOT texture approval or native integration'))
    print('Editable mesh validation passed:',len(candidate['vertices']),'vertices,',len(candidate['faces']),'unchanged indexed faces/UV arrays')
    print('Editable manifest SHA256',b.a.sha(out/'manifest.json'))


def validate(original,candidate):
    mapping=dict(json.loads((b.HERE/'z-map.json').read_text())['anchors'])
    assert original['faces']==candidate['faces'], 'Topology, UV or face metadata changed'
    restored=copy.deepcopy(candidate)
    for old,new in zip(original['vertices'],restored['vertices']):
        assert old[:2]==new[:2]
        assert new[2]==mapping[old[2]]
        new[2]=old[2]
    assert candidate['height']==mapping[original['height']], 'Undeclared authored height'
    restored['height']=original['height']
    assert restored==original, 'Non-Z source metadata changed'
    proxy=json.loads((b.HERE/'output/proposed-geometry.json').read_text())[0]
    for indexed,flat in zip(candidate['faces'],proxy['faces']):
        assert indexed['name']==flat['name']
        assert [candidate['vertices'][i] for i in indexed['indices']]==flat['vertices']
    assert len(candidate['faces'])==len(proxy['faces'])


def report():
    data=json.loads((b.HERE/'output/dimension-diff.json').read_text())
    rows=['# Kiosk-only dimension and spacing diff','','All values are authored world units, not meters. Player49.5 is source root-to-alpha-top visual reference, not stature. Camera full registered canvas height103.34928229665071 is not physical pole height.','','| Kiosk measure | Current | Candidate | Delta | Current / Player | Candidate / Player |','|---|---:|---:|---:|---:|---:|']
    for name,row in data['dimensions'].items():
        rows.append(f"| {name} | {row['current']:.6f} | {row['proposed']:.6f} | {row['delta']:+.6f} | {row['currentPlayerRatio']:.6f} | {row['proposedPlayerRatio']:.6f} |")
    rows.extend(['','Entry remains blocked under authority, not a traversable door. Recess depths remain8.2 for entry and3.2 for windows. Chamfer39 and all XY subdivisions remain exact. No topology changes.','','## Complete Z map','','| Current Z | Candidate Z |','|---:|---:|'])
    for old,new in data['zMap']['anchors']:rows.append(f'| {old:.15g} | {new:.15g} |')
    rows.extend(['','## Unchanged plan relationships','','Camera root[496,672] is16 from the kiosk authority rectangle. Player root[736,654] is96 from it. All roots, actors, Camera fields, and registered dimensions stay fixed.','','| Unchanged neighbor | X gap | Y gap | Envelope distance | Authored height |','|---|---:|---:|---:|---:|'])
    for name,row in data['spacing']['neighbors'].items():
        rows.append(f"| {name} | {row['axisGaps'][0]} | {row['axisGaps'][1]} | {row['envelopeDistance']:.6f} | {row['authoredHeight']} |")
    rows.extend(['','Envelope distances do not establish pavement setbacks, physical clearances or architectural quality. The kiosk and northern residential envelope meet at[512,768]. Visible chamfer contour differs from rectangular collision. The zero-gap relationship remains unresolved under fixed XY scope.','','## Editable files','','`current-indexed-mesh.json` is an exact byte copy of the V9 kiosk source mesh. `candidate-indexed-mesh.json` retains schema, all face indices, UVs, hidden flags, materials, XY and metadata, modifying only vertex Z and height132 to104. Both are review-only. Existing texture UVs may compress painted detail under the new Z spacing, so no textured/native result is certified. The rendered proxy uses flat materials, not those textures.',''])
    return '\n'.join(rows)


if __name__=='__main__':
    export(b.HERE/'editable')
