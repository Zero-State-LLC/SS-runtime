"""Generate dimension/massing audit from fixed comparison geometry, no render or art edit."""
import hashlib
import json
from pathlib import Path

HERE=Path(__file__).resolve().parent
OUT=HERE/'output'


def load(name):
    return json.loads((OUT/name).read_text())


def area_xy(vertices):
    return abs(sum(a[0]*b[1]-b[0]*a[1] for a,b in zip(vertices,vertices[1:]+vertices[:1])))/2


def massing(building):
    """Measure explicitly authored roof plan and cornice profile, not physical mass."""
    role=building['solidID']
    faces=building['faces']
    vertices=[v for f in faces for v in f['vertices']]
    lo=[min(v[i] for v in vertices) for i in range(3)]
    hi=[max(v[i] for v in vertices) for i in range(3)]
    if 'kiosk' in role:
        roof=[f for f in faces if f['name']=='recessed-roof']
        cap=[f for f in faces if f['name'].startswith('parapet-cap-')]
        roof_z=roof[0]['vertices'][0][2]
        top=max(v[2] for f in cap for v in f['vertices'])
        cap_area=sum(area_xy(f['vertices']) for f in cap)
        mass=dict(roofPlanArea=sum(area_xy(f['vertices']) for f in roof),roofDeckZ=roof_z,parapetRise=top-roof_z,copingPlanArea=cap_area,parapetPrismEquivalentVolume=cap_area*(top-roof_z),qualification='Prism-equivalent cap area times inner parapet rise, not solid-union or material mass. Exterior facade relief remains nonuniform. Roof deck is a face, not an authored slab thickness.')
    elif 'dais' in role:
        roof=[f for f in faces if f['name'].startswith('raised-paving/roof')]
        mass=dict(platformPlanArea=sum(area_xy(f['vertices']) for f in roof),qualification='Open raised platform. No roof slab, cornice or enclosed volume implied.')
    else:
        roof=[f for f in faces if f['name'].startswith('masonry-shell/roof')]
        # Each author.py strip is a closed rectangular prism. Report sum, not union.
        groups={}
        for f in faces:
            if f['name'].startswith(('eaves','parapet','coping')):
                groups.setdefault(f['name'].split('/')[0],[]).extend(f['vertices'])
        volume=0
        for vs in groups.values():
            lengths=[max(v[i] for v in vs)-min(v[i] for v in vs) for i in range(3)]
            volume+=lengths[0]*lengths[1]*lengths[2]
        mass=dict(roofPlanArea=sum(area_xy(f['vertices']) for f in roof),cornicePrismVolumeSum=volume,qualification='Sum of original eaves/parapet/coping box volumes. Corner intersections are counted per box, not a boolean-union or physical mass. Roof deck face has no separate slab-thickness claim.')
    return dict(meshBoundsLocalXYZ=[lo,hi],meshWidth=hi[0]-lo[0],meshDepth=hi[1]-lo[1],**mass)


def main():
    dimensions=load('dimensions.json')
    old,new=load('current-geometry.json'),load('proposed-geometry.json')
    entries=[]
    lines=['# Architectural dimension and massing report','',
           'BP-001/007/012, T1045. One initial proposal with two technical adapter corrections. No owner acceptance or native execution. All dimensions are authored world units, not meters.','',
           '## Unchanged scale reference','',
           'Player root-to-alpha-top = **49.5** world units, measured from source rootY336 minus alpha top39 at6 source pixels per world unit. Full nonzero-alpha span =53.3333. Alpha includes painted rendering and is not physical stature. Retained full Player canvas remains64x69.3333, Camera46.8517x103.3493. No actor scaling or relocation is used.','',
           'Player ratios below use49.5, so doorway clearance1.25 means1.25 times this visual reference, not a certified human clearance.','',
           '## Limits that remain open','',
           '- Residential-west, residential-north and civic-west meshes contain glazing bays, not explicit doorways. No plausible doorway clearance can be claimed for those sources and none was invented in this vertical-only comparison.',
           '- Kiosk entry remains within a blocked authoritative rectangle. Its recessed aperture is a visual opening, not a traversable route. The retained blocked-base supplement is18 high and now coincides with the proposed entry threshold18.',
           '- Roof/cornice mass is reported as visible vertical profile, unchanged plan area and qualified geometric volume proxies. No material densities or real-world mass are claimed.',
           '- Dais has no doorway, story, window, facade or roof. Platform and rail dimensions are reported instead.',
           '- All XY vertices, recess offsets, footprints, contact vertices and roots remain exact. Ratios do not establish visual approval.','']
    for row,a,b in zip(dimensions['buildings'],old,new):
        entry=dict(solidID=row['solidID'],current=massing(a),proposed=massing(b))
        entries.append(entry)
        lines.extend(['## '+row['solidID'],'',row['doorwayQualification'],'',
                      '| Dimension | Current | Proposed | Change | Current / Player | Proposed / Player |',
                      '|---|---:|---:|---:|---:|---:|'])
        for name,v in row['dimensions'].items():
            lines.append(f"| {name} | {v['current']:.4f} | {v['proposed']:.4f} | {v['delta']:+.4f} | {v['currentPlayerRatio']:.4f} | {v['proposedPlayerRatio']:.4f} |")
        lines.extend(['','### Roof / cornice plan and massing','',entry['current']['qualification'],'',
                      '| Measured geometry | Current | Proposed |','|---|---:|---:|'])
        for key,value in entry['current'].items():
            if isinstance(value,(float,int)):
                lines.append(f"| {key} | {value:.4f} | {entry['proposed'][key]:.4f} |")
        lines.extend(['','### Complete vertical subdivision mapping','',
                      'Every baseline vertex Z is mapped below. X and Y are unchanged, topology is unchanged, and the maps are monotone but deliberately nonuniform.','',
                      '| Baseline Z | Proposed Z |','|---:|---:|'])
        lines.extend(f"| {m['current']:.6f} | {m['proposed']:.6f} |" for m in row['verticalSubdivisionMap'])
        lines.append('')
    lines.extend(['## Scene and depth','',
                  'All71 V9 items remain in the imported authoritative footprint-depth ordering, including9 offcrop legacy actors. The same order and constraints are checked exactly against retained V9 records. Five source buildings are replaced by newly rasterized flat meshes, never by scaling old building images. Camera remains in front of kiosk where the authoritative separation orders it there.',
                  '', 'Source composition starts from the registered ground image using square tileUnits2304 and texture crop[0,0,1,2/3]. No native screenshot supplies pixels beneath a changed building, so a reduced silhouette cannot expose old textured ghost pixels.','',
                  'Source proxy omissions: native HUD/touch controls, native Player shadow and raster kiosk roof vent. Camera field geometry is retained but raster styling is a proxy. The untouched V9 native and full original benchmark are separate comparison panes.','',
                  '## Reproduction','',
                  '```sh',
                  'PYTHONDONTWRITEBYTECODE=1 python3 docs/review/architectural-scale-20261117/source/build.py --out <new-empty-source-output-path>',
                  'PYTHONDONTWRITEBYTECODE=1 python3 docs/review/architectural-scale-20261117/source/test_source.py',
                  'PYTHONDONTWRITEBYTECODE=1 python3 docs/review/architectural-scale-20261117/source/report_dimensions.py',
                  '```','',
                  'Existing output paths fail closed to prevent silent overwriting. The first failed ground-UV output is retained under attempt-01-ground-uv, and the corrected-ground/incorrect-normal intermediate under attempt-02-face-normals. Tests establish source geometry/registration/compositing integrity, not independent aesthetic approval.'])
    (HERE/'DIMENSIONS.md').write_text('\n'.join(lines)+'\n')
    evidence=dict(sourceGeometrySHA256={name:hashlib.sha256((OUT/name).read_bytes()).hexdigest() for name in ('current-geometry.json','proposed-geometry.json')},buildings=entries)
    (HERE/'massing-measurements.json').write_text(json.dumps(evidence,indent=2)+'\n')
    print('DIMENSIONS.md and massing-measurements.json generated from fixed geometry.')


if __name__=='__main__':
    main()
