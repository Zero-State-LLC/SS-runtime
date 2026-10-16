# BP-004/BP-007 camera source re-export

Runtime base: 385a06f. Spec pin: 00ce027209e6c233bcdd35295f35f0b9bfb9bbe5. REVIEW ONLY; no shipping asset or clip migration.

Four 384×576 RGBA exports come directly from the existing 2048×768 municipal state source, using uniform scale 468/658 (0.7112462). These are downsampled source cells, not enlarged 256×384 exports. The same alpha cleanup and source base registration are retained. Ground anchor becomes (192,528), equivalent to the existing logical (32,88) on a 64×96 canvas. No housing, material, damage design or pose was regenerated.

The comparison shows old (top) and source re-export (bottom) at identical 272×408 output size, approximating the closer √2 framing at the current 3× backing scale. It is an offline sampling comparison, not a SpriteKit capture. Viewed at this size, the improvement is modest: edges and damage detail retain slightly more definition. The existing design remains intact.

New exports provide about 1.41 source pixels per output pixel at that closer framing. Four RGBA8 canvases represent 3,538,944 raw bytes versus 1,572,864 for the previous four: 2.25× texels. These figures exclude atlas packing, mipmaps, compression and other GPU allocations, and are not measured residency.

Remaining blockers: the permanent pole/base is not pixel-identical across the generated states; the six required clips and their distinct frames are incomplete; transition/interruption/Reduced Motion and actual-renderer visual acceptance are not established by this comparison. No physical-device testing occurred. Keep the new exports as candidates until a real-renderer comparison and complete camera delivery satisfy BP-004/BP-006.

Reproduce: `python3 export.py source.png export-directory previous-directory`, where previous-directory contains intact.png, damaged.png, critical.png and destroyed.png from the original state study. Source SHA-256 and export hashes are in registration.json. Existing source prompt is copied to source-prompt.txt; generation used the built-in image tool in the earlier state study. This revision uses only the user's authorized deterministic cleanup/registration/export, with no new image-generation call.
