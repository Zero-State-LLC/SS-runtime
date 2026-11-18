# Stone corner: slice 3 building registration

**Status: PROVISIONAL_DIAGNOSTIC_MISSING_CORRESPONDENCE. Not ready for native. Not owner accepted. Not production admitted.**

This packet records the first registration attempt for the generated stone-corner building source (`stone-corner-source-20261116/`). The original source PNG and its SHA256 are preserved unchanged.

## What is actually visible

The source contains no rendered ground surface. The building floats on a transparent background. There is no wall-meets-ground junction visible in the image.

What can be identified visually:
- **Stone plinth/base course**: a rendered base band at the foot of each wall face, terminating sharply into transparency (alpha drops from ~251 to ~62 to ~3 within 4 pixels at the base edge).
- **Stair/apron**: three descending steps beneath the chamfered entrance, identifiable visually.
- **Roof ridge and wall faces**: visible structure above the plinth.
- **Hidden rear vertices**: not visible and not inferred from roof or alpha.

## What was measured

The plinth-base painted edge was measured as a provisional diagnostic -- not as wall-ground contact:

| Face | Observed edge | Plinth-base slope | Reference ground slope | Difference |
|------|---------------|-------------------|----------------------|------------|
| Left | (142,922) to (~400,1078) | +0.600 | +0.500 | 0.100 |
| Right | (1111,914) to (~840,1082) | -0.608 | -0.500 | 0.108 |

Fit residuals within each line are low (left max 2.8 px RMS 1.4; right max 6.1 px RMS 2.7). The slope difference is noted but **not confirmed as a source defect** -- it may reflect the plinth geometry itself, a baked perspective tilt, or a genuinely steeper ground angle. Without a visible wall-ground junction, slope comparison to the +/-0.5 ground matrix cannot be used to prove or disprove registrability.

Stair/apron: flat bottom y=1139, x=480..740. Identified visually, excluded from wall-footprint measurement.

## Actual blocker

**Missing correspondence.** No visible wall-meets-ground junction means the source-to-world correspondence cannot be established from this image alone. Neither prompted footprint coordinates (not measurements) nor plinth-base alpha edges (not ground contact) can substitute for real wall-ground landmarks.

This is distinct from a claimed geometry mismatch: the plinth slope observation is a provisional diagnostic, not proof that the source cannot be registered.

## What is NOT claimed

- The slope difference is NOT confirmed as a source defect.
- The plinth-base edge is NOT wall-ground contact.
- Hidden vertices have NOT been reconstructed from roof or alpha bounds.
- No fallback primitive has been integrated.

## Outputs

| File | Description |
|------|-------------|
| `registration.json` | Full record: null landmarks, provisional plinth diagnostic, blocker |
| `landmark-overlay.png` | Source with plinth-base edges (green) and stair (yellow) annotated |
| `index.html` | Corrected native-pixel original/contour comparison with explicit uncertainty |
| `withdrawn/` | Historical PNG previews with invalid baked-in contact/scale captions, not evidence |
| `test_registration.py` | Five packet-consistency tests, not geometry or fidelity tests |

## Running the tests

```
python3 -B -W error::ResourceWarning docs/review/stone-corner-registration-20261116/test_registration.py
```

Uses Python standard library only. Passing these checks confirms internal consistency only.

## Correction history

The initial report incorrectly elevated alpha-derived contours to wall-contact measurements and declared a source defect. Those conclusions are withdrawn. No manually verified structural wall-ground correspondence is supplied. Absence of a rendered ground plane alone is not proof that registration is impossible. The available evidence does not identify which visible base edge corresponds to the existing solid. The overlay retains provisional contour samples and prompt targets only. Stair endpoint and connecting-segment labels likewise do not establish structural junctions. Source fidelity remains independently unassessed. No new source, production change, native run, commit or push accompanies this correction.
