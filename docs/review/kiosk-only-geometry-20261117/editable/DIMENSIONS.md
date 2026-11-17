# Kiosk-only dimension and spacing diff

All values are authored world units, not meters. Player49.5 is source root-to-alpha-top visual reference, not stature. Camera full registered canvas height103.34928229665071 is not physical pole height.

| Kiosk measure | Current | Candidate | Delta | Current / Player | Candidate / Player |
|---|---:|---:|---:|---:|---:|
| top | 132.000000 | 104.000000 | -28.000000 | 2.666667 | 2.101010 |
| roofDeck | 125.000000 | 100.000000 | -25.000000 | 2.525253 | 2.020202 |
| parapet | 7.000000 | 4.000000 | -3.000000 | 0.141414 | 0.080808 |
| cornice | 24.217054 | 10.000000 | -14.217054 | 0.489233 | 0.202020 |
| doorThreshold | 27.116279 | 18.000000 | -9.116279 | 0.547804 | 0.363636 |
| doorHead | 92.775194 | 80.000000 | -12.775194 | 1.874246 | 1.616162 |
| doorClearance | 65.658915 | 62.000000 | -3.658915 | 1.326443 | 1.252525 |
| windowSill | 43.658915 | 32.000000 | -11.658915 | 0.881998 | 0.646465 |
| windowHead | 92.775194 | 80.000000 | -12.775194 | 1.874246 | 1.616162 |
| windowHeight | 49.116279 | 48.000000 | -1.116279 | 0.992248 | 0.969697 |
| width | 128.000000 | 128.000000 | +0.000000 | 2.585859 | 2.585859 |
| depth | 128.000000 | 128.000000 | +0.000000 | 2.585859 | 2.585859 |

Entry remains blocked under authority, not a traversable door. Recess depths remain8.2 for entry and3.2 for windows. Chamfer39 and all XY subdivisions remain exact. No topology changes.

## Complete Z map

| Current Z | Candidate Z |
|---:|---:|
| 0 | 0 |
| 7.67441860465116 | 5 |
| 17.7364341085271 | 10 |
| 27.1162790697674 | 18 |
| 31.3798449612403 | 21 |
| 38.5426356589147 | 25 |
| 43.6589147286822 | 32 |
| 72.3100775193798 | 60 |
| 92.7751937984496 | 80 |
| 95.3333333333333 | 82 |
| 102.325581395349 | 88 |
| 107.782945736434 | 94 |
| 122.790697674419 | 99 |
| 125 | 100 |
| 126.883720930233 | 101 |
| 132 | 104 |

## Unchanged plan relationships

Camera root[496,672] is16 from the kiosk authority rectangle. Player root[736,654] is96 from it. All roots, actors, Camera fields, and registered dimensions stay fixed.

| Unchanged neighbor | X gap | Y gap | Envelope distance | Authored height |
|---|---:|---:|---:|---:|
| solid-01-residential-west | 384 | 0 | 384.000000 | 112 |
| solid-02-residential-north | 0 | 0 | 0.000000 | 112 |
| solid-04-civic-west | 96 | 0 | 96.000000 | 142 |
| solid-05-civic-dais | 368 | 0 | 368.000000 | 34 |

Envelope distances do not establish pavement setbacks, physical clearances or architectural quality. The kiosk and northern residential envelope meet at[512,768]. Visible chamfer contour differs from rectangular collision. The zero-gap relationship remains unresolved under fixed XY scope.

## Editable files

`current-indexed-mesh.json` is an exact byte copy of the V9 kiosk source mesh. `candidate-indexed-mesh.json` retains schema, all face indices, UVs, hidden flags, materials, XY and metadata, modifying only vertex Z and height132 to104. Both are review-only. Existing texture UVs may compress painted detail under the new Z spacing, so no textured/native result is certified. The rendered proxy uses flat materials, not those textures.
