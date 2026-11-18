# Architectural dimension and massing report

BP-001/007/012, T1045. One initial proposal with two technical adapter corrections. No owner acceptance or native execution. All dimensions are authored world units, not meters.

## Unchanged scale reference

Player root-to-alpha-top = **49.5** world units, measured from source rootY336 minus alpha top39 at6 source pixels per world unit. Full nonzero-alpha span =53.3333. Alpha includes painted rendering and is not physical stature. Retained full Player canvas remains64x69.3333, Camera46.8517x103.3493. No actor scaling or relocation is used.

Player ratios below use49.5, so doorway clearance1.25 means1.25 times this visual reference, not a certified human clearance.

## Limits that remain open

- Residential-west, residential-north and civic-west meshes contain glazing bays, not explicit doorways. No plausible doorway clearance can be claimed for those sources and none was invented in this vertical-only comparison.
- Kiosk entry remains within a blocked authoritative rectangle. Its recessed aperture is a visual opening, not a traversable route. The retained blocked-base supplement is18 high and now coincides with the proposed entry threshold18.
- Roof/cornice mass is reported as visible vertical profile, unchanged plan area and qualified geometric volume proxies. No material densities or real-world mass are claimed.
- Dais has no doorway, story, window, facade or roof. Platform and rail dimensions are reported instead.
- All XY vertices, recess offsets, footprints, contact vertices and roots remain exact. Ratios do not establish visual approval.

## solid-03-transit-kiosk

Recessed entry aperture only, not gameplay traversal. Preserved blocked rectangle.

| Dimension | Current | Proposed | Change | Current / Player | Proposed / Player |
|---|---:|---:|---:|---:|---:|
| facadeTop | 132.0000 | 104.0000 | -28.0000 | 2.6667 | 2.1010 |
| roofDeck | 125.0000 | 100.0000 | -25.0000 | 2.5253 | 2.0202 |
| parapetHeight | 7.0000 | 4.0000 | -3.0000 | 0.1414 | 0.0808 |
| corniceZoneHeight | 24.2171 | 10.0000 | -14.2171 | 0.4892 | 0.2020 |
| doorThreshold | 27.1163 | 18.0000 | -9.1163 | 0.5478 | 0.3636 |
| doorHead | 92.7752 | 80.0000 | -12.7752 | 1.8742 | 1.6162 |
| doorClearance | 65.6589 | 62.0000 | -3.6589 | 1.3264 | 1.2525 |
| windowSill | 43.6589 | 32.0000 | -11.6589 | 0.8820 | 0.6465 |
| windowHead | 92.7752 | 80.0000 | -12.7752 | 1.8742 | 1.6162 |
| windowHeight | 49.1163 | 48.0000 | -1.1163 | 0.9922 | 0.9697 |
| storeyHeight | 132.0000 | 104.0000 | -28.0000 | 2.6667 | 2.1010 |
| doorRecessDepth | 8.2000 | 8.2000 | +0.0000 | 0.1657 | 0.1657 |
| windowRecessDepth | 3.2000 | 3.2000 | +0.0000 | 0.0646 | 0.0646 |
| footprintWidth | 128.0000 | 128.0000 | +0.0000 | 2.5859 | 2.5859 |
| footprintDepth | 128.0000 | 128.0000 | +0.0000 | 2.5859 | 2.5859 |

### Roof / cornice plan and massing

Prism-equivalent cap area times inner parapet rise, not solid-union or material mass. Exterior facade relief remains nonuniform. Roof deck is a face, not an authored slab thickness.

| Measured geometry | Current | Proposed |
|---|---:|---:|
| meshWidth | 128.0000 | 128.0000 |
| meshDepth | 128.0000 | 128.0000 |
| roofPlanArea | 14097.4092 | 14097.4092 |
| roofDeckZ | 125.0000 | 100.0000 |
| parapetRise | 7.0000 | 4.0000 |
| copingPlanArea | 1526.0908 | 1526.0908 |
| parapetPrismEquivalentVolume | 10682.6353 | 6104.3630 |

### Complete vertical subdivision mapping

Every baseline vertex Z is mapped below. X and Y are unchanged, topology is unchanged, and the maps are monotone but deliberately nonuniform.

| Baseline Z | Proposed Z |
|---:|---:|
| 0.000000 | 0.000000 |
| 7.674419 | 5.000000 |
| 17.736434 | 10.000000 |
| 27.116279 | 18.000000 |
| 31.379845 | 21.000000 |
| 38.542636 | 25.000000 |
| 43.658915 | 32.000000 |
| 72.310078 | 60.000000 |
| 92.775194 | 80.000000 |
| 95.333333 | 82.000000 |
| 102.325581 | 88.000000 |
| 107.782946 | 94.000000 |
| 122.790698 | 99.000000 |
| 125.000000 | 100.000000 |
| 126.883721 | 101.000000 |
| 132.000000 | 104.000000 |

## solid-01-residential-west

NO EXPLICIT DOORWAY IN BASELINE MESH. Clearance cannot be inferred from windows. None invented.

| Dimension | Current | Proposed | Change | Current / Player | Proposed / Player |
|---|---:|---:|---:|---:|---:|
| facadeTop | 112.0000 | 150.0000 | +38.0000 | 2.2626 | 3.0303 |
| roofDeck | 112.0000 | 150.0000 | +38.0000 | 2.2626 | 3.0303 |
| corniceZoneHeight | 13.0000 | 11.0000 | -2.0000 | 0.2626 | 0.2222 |
| copingTop | 121.0000 | 157.0000 | +36.0000 | 2.4444 | 3.1717 |
| chimneyTop | 136.0000 | 172.0000 | +36.0000 | 2.7475 | 3.4747 |
| windowHeight | 35.0000 | 40.0000 | +5.0000 | 0.7071 | 0.8081 |
| storeyPitch | 46.0000 | 66.0000 | +20.0000 | 0.9293 | 1.3333 |
| groundWindowSill | 15.0000 | 20.0000 | +5.0000 | 0.3030 | 0.4040 |
| groundWindowHead | 50.0000 | 60.0000 | +10.0000 | 1.0101 | 1.2121 |
| upperWindowSill | 61.0000 | 86.0000 | +25.0000 | 1.2323 | 1.7374 |
| upperWindowHead | 96.0000 | 126.0000 | +30.0000 | 1.9394 | 2.5455 |
| footprintWidth | 128.0000 | 128.0000 | +0.0000 | 2.5859 | 2.5859 |
| footprintDepth | 512.0000 | 512.0000 | +0.0000 | 10.3434 | 10.3434 |

### Roof / cornice plan and massing

Sum of original eaves/parapet/coping box volumes. Corner intersections are counted per box, not a boolean-union or physical mass. Roof deck face has no separate slab-thickness claim.

| Measured geometry | Current | Proposed |
|---|---:|---:|
| meshWidth | 128.0000 | 128.0000 |
| meshDepth | 512.0000 | 512.0000 |
| roofPlanArea | 61732.0000 | 61732.0000 |
| cornicePrismVolumeSum | 33184.0000 | 28096.0000 |

### Complete vertical subdivision mapping

Every baseline vertex Z is mapped below. X and Y are unchanged, topology is unchanged, and the maps are monotone but deliberately nonuniform.

| Baseline Z | Proposed Z |
|---:|---:|
| 0.000000 | 0.000000 |
| 5.000000 | 5.000000 |
| 7.000000 | 7.000000 |
| 10.000000 | 10.000000 |
| 11.000000 | 16.000000 |
| 13.000000 | 18.000000 |
| 15.000000 | 20.000000 |
| 50.000000 | 60.000000 |
| 53.000000 | 63.000000 |
| 55.000000 | 70.000000 |
| 57.000000 | 72.000000 |
| 58.000000 | 73.000000 |
| 59.000000 | 84.000000 |
| 61.000000 | 86.000000 |
| 96.000000 | 126.000000 |
| 99.000000 | 129.000000 |
| 108.000000 | 146.000000 |
| 112.000000 | 150.000000 |
| 113.000000 | 151.000000 |
| 119.000000 | 155.000000 |
| 121.000000 | 157.000000 |
| 134.000000 | 170.000000 |
| 136.000000 | 172.000000 |

## solid-02-residential-north

NO EXPLICIT DOORWAY IN BASELINE MESH. Clearance cannot be inferred from windows. None invented.

| Dimension | Current | Proposed | Change | Current / Player | Proposed / Player |
|---|---:|---:|---:|---:|---:|
| facadeTop | 112.0000 | 150.0000 | +38.0000 | 2.2626 | 3.0303 |
| roofDeck | 112.0000 | 150.0000 | +38.0000 | 2.2626 | 3.0303 |
| corniceZoneHeight | 13.0000 | 11.0000 | -2.0000 | 0.2626 | 0.2222 |
| copingTop | 121.0000 | 157.0000 | +36.0000 | 2.4444 | 3.1717 |
| chimneyTop | 136.0000 | 172.0000 | +36.0000 | 2.7475 | 3.4747 |
| windowHeight | 35.0000 | 40.0000 | +5.0000 | 0.7071 | 0.8081 |
| storeyPitch | 46.0000 | 66.0000 | +20.0000 | 0.9293 | 1.3333 |
| groundWindowSill | 15.0000 | 20.0000 | +5.0000 | 0.3030 | 0.4040 |
| groundWindowHead | 50.0000 | 60.0000 | +10.0000 | 1.0101 | 1.2121 |
| upperWindowSill | 61.0000 | 86.0000 | +25.0000 | 1.2323 | 1.7374 |
| upperWindowHead | 96.0000 | 126.0000 | +30.0000 | 1.9394 | 2.5455 |
| footprintWidth | 384.0000 | 384.0000 | +0.0000 | 7.7576 | 7.7576 |
| footprintDepth | 192.0000 | 192.0000 | +0.0000 | 3.8788 | 3.8788 |

### Roof / cornice plan and massing

Sum of original eaves/parapet/coping box volumes. Corner intersections are counted per box, not a boolean-union or physical mass. Roof deck face has no separate slab-thickness claim.

| Measured geometry | Current | Proposed |
|---|---:|---:|
| meshWidth | 384.0000 | 384.0000 |
| meshDepth | 192.0000 | 192.0000 |
| roofPlanArea | 70308.0000 | 70308.0000 |
| cornicePrismVolumeSum | 29856.0000 | 25280.0000 |

### Complete vertical subdivision mapping

Every baseline vertex Z is mapped below. X and Y are unchanged, topology is unchanged, and the maps are monotone but deliberately nonuniform.

| Baseline Z | Proposed Z |
|---:|---:|
| 0.000000 | 0.000000 |
| 5.000000 | 5.000000 |
| 7.000000 | 7.000000 |
| 10.000000 | 10.000000 |
| 11.000000 | 16.000000 |
| 13.000000 | 18.000000 |
| 15.000000 | 20.000000 |
| 50.000000 | 60.000000 |
| 53.000000 | 63.000000 |
| 55.000000 | 70.000000 |
| 57.000000 | 72.000000 |
| 58.000000 | 73.000000 |
| 59.000000 | 84.000000 |
| 61.000000 | 86.000000 |
| 96.000000 | 126.000000 |
| 99.000000 | 129.000000 |
| 108.000000 | 146.000000 |
| 112.000000 | 150.000000 |
| 113.000000 | 151.000000 |
| 119.000000 | 155.000000 |
| 121.000000 | 157.000000 |
| 134.000000 | 170.000000 |
| 136.000000 | 172.000000 |

## solid-04-civic-west

NO EXPLICIT DOORWAY IN BASELINE MESH. Clearance unmeasurable. None invented.

| Dimension | Current | Proposed | Change | Current / Player | Proposed / Player |
|---|---:|---:|---:|---:|---:|
| facadeTop | 142.0000 | 120.0000 | -22.0000 | 2.8687 | 2.4242 |
| roofDeck | 142.0000 | 120.0000 | -22.0000 | 2.8687 | 2.4242 |
| corniceZoneHeight | 13.0000 | 11.0000 | -2.0000 | 0.2626 | 0.2222 |
| copingTop | 151.0000 | 127.0000 | -24.0000 | 3.0505 | 2.5657 |
| lanternTop | 156.0000 | 134.0000 | -22.0000 | 3.1515 | 2.7071 |
| windowSill | 15.0000 | 20.0000 | +5.0000 | 0.3030 | 0.4040 |
| windowHead | 111.0000 | 84.0000 | -27.0000 | 2.2424 | 1.6970 |
| windowHeight | 96.0000 | 64.0000 | -32.0000 | 1.9394 | 1.2929 |
| storeyHeight | 142.0000 | 120.0000 | -22.0000 | 2.8687 | 2.4242 |
| footprintWidth | 192.0000 | 192.0000 | +0.0000 | 3.8788 | 3.8788 |
| footprintDepth | 384.0000 | 384.0000 | +0.0000 | 7.7576 | 7.7576 |

### Roof / cornice plan and massing

Sum of original eaves/parapet/coping box volumes. Corner intersections are counted per box, not a boolean-union or physical mass. Roof deck face has no separate slab-thickness claim.

| Measured geometry | Current | Proposed |
|---|---:|---:|
| meshWidth | 192.0000 | 192.0000 |
| meshDepth | 384.0000 | 384.0000 |
| roofPlanArea | 70308.0000 | 70308.0000 |
| cornicePrismVolumeSum | 29856.0000 | 25280.0000 |

### Complete vertical subdivision mapping

Every baseline vertex Z is mapped below. X and Y are unchanged, topology is unchanged, and the maps are monotone but deliberately nonuniform.

| Baseline Z | Proposed Z |
|---:|---:|
| 0.000000 | 0.000000 |
| 5.000000 | 5.000000 |
| 7.000000 | 7.000000 |
| 10.000000 | 10.000000 |
| 11.000000 | 16.000000 |
| 13.000000 | 18.000000 |
| 15.000000 | 20.000000 |
| 111.000000 | 84.000000 |
| 113.000000 | 86.000000 |
| 114.000000 | 87.000000 |
| 119.000000 | 94.000000 |
| 138.000000 | 116.000000 |
| 142.000000 | 120.000000 |
| 143.000000 | 121.000000 |
| 146.000000 | 124.000000 |
| 149.000000 | 125.000000 |
| 151.000000 | 127.000000 |
| 156.000000 | 134.000000 |

## solid-05-civic-dais

Not applicable: open dais, no facade, doorway, windows, story or roof.

| Dimension | Current | Proposed | Change | Current / Player | Proposed / Player |
|---|---:|---:|---:|---:|---:|
| platformHeight | 13.0000 | 9.0000 | -4.0000 | 0.2626 | 0.1818 |
| railTop | 34.0000 | 35.0000 | +1.0000 | 0.6869 | 0.7071 |
| railAbovePlatform | 21.0000 | 26.0000 | +5.0000 | 0.4242 | 0.5253 |
| topRailThickness | 3.0000 | 3.0000 | +0.0000 | 0.0606 | 0.0606 |
| firstStepHeight | 5.0000 | 3.0000 | -2.0000 | 0.1010 | 0.0606 |
| secondStepRise | 4.0000 | 3.0000 | -1.0000 | 0.0808 | 0.0606 |
| footprintWidth | 160.0000 | 160.0000 | +0.0000 | 3.2323 | 3.2323 |
| footprintDepth | 96.0000 | 96.0000 | +0.0000 | 1.9394 | 1.9394 |

### Roof / cornice plan and massing

Open raised platform. No roof slab, cornice or enclosed volume implied.

| Measured geometry | Current | Proposed |
|---|---:|---:|
| meshWidth | 160.0000 | 160.0000 |
| meshDepth | 96.0000 | 96.0000 |
| platformPlanArea | 11520.0000 | 11520.0000 |

### Complete vertical subdivision mapping

Every baseline vertex Z is mapped below. X and Y are unchanged, topology is unchanged, and the maps are monotone but deliberately nonuniform.

| Baseline Z | Proposed Z |
|---:|---:|
| 0.000000 | 0.000000 |
| 5.000000 | 3.000000 |
| 9.000000 | 6.000000 |
| 13.000000 | 9.000000 |
| 16.000000 | 12.000000 |
| 31.000000 | 32.000000 |
| 34.000000 | 35.000000 |

## Scene and depth

All71 V9 items remain in the imported authoritative footprint-depth ordering, including9 offcrop legacy actors. The same order and constraints are checked exactly against retained V9 records. Five source buildings are replaced by newly rasterized flat meshes, never by scaling old building images. Camera remains in front of kiosk where the authoritative separation orders it there.

Source composition starts from the registered ground image using square tileUnits2304 and texture crop[0,0,1,2/3]. No native screenshot supplies pixels beneath a changed building, so a reduced silhouette cannot expose old textured ghost pixels.

Source proxy omissions: native HUD/touch controls, native Player shadow and raster kiosk roof vent. Camera field geometry is retained but raster styling is a proxy. The untouched V9 native and full original benchmark are separate comparison panes.

## Reproduction

```sh
PYTHONDONTWRITEBYTECODE=1 python3 docs/review/architectural-scale-20261117/source/build.py --out <new-empty-source-output-path>
PYTHONDONTWRITEBYTECODE=1 python3 docs/review/architectural-scale-20261117/source/test_source.py
PYTHONDONTWRITEBYTECODE=1 python3 docs/review/architectural-scale-20261117/source/report_dimensions.py
```

Existing output paths fail closed to prevent silent overwriting. The first failed ground-UV output is retained under attempt-01-ground-uv, and the corrected-ground/incorrect-normal intermediate under attempt-02-face-normals. Tests establish source geometry/registration/compositing integrity, not independent aesthetic approval.
