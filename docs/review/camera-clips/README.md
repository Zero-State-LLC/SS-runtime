# BP-004 six camera clip source candidates

Status: source preview; not runtime admission. Spec proposal ea35222 follows active BP-004 at 521aec3. Source comes from shared municipal camera structure e8193bd.

All six existing clip IDs and 16 frame slots are exported with exact v1 frame order and duration fractions in clips.json. Operational:4/6s; hit:2/16s; critical-entry:3/12s; destruction:4/12s; field-off:1/12s; destroyed-idle:2/4s. No timing or production metadata changed.

Source controls are in parameters.json; build.py regenerates PNGs and checks. All pixels outside the authored head mask remain identical to intact. Every non-operational clip terminates at the exact corresponding settled state. Destruction frames contain no cyan indicator pixels by the documented RGB predicate; this narrow pixel check is not an accessibility certification. Two destroyed-idle holds are deliberately identical. Operational repeats its intermediate indicator level to close the loop; unique hashes are not a quality criterion.

index.html provides normal/quarter-speed playback, pause, frame advance, Reduced Motion settled preview and grayscale. Browser interaction verified clip selection, replay, reduced preview and grayscale. Contact sheet visually inspected: mount is stable, stage damage is readable in the large source, effects are restrained. Destruction fragments are subtle at native size and still require runtime judgment. These previews do not prove real SpriteKit timing, interruption, latest-integrity arbitration, field removal, encounter readability or performance.

Research and authored choices are separated in design.md. Six clip source candidates are now available for the real-renderer review fixture. The game and its test-bundle assets remain unchanged. Full character, environment, benchmark composition and device gates remain open. No new app/core test run is claimed for this offline source change.

Reproduce with Python 3 + Pillow: python3 build.py. Serve this directory or open index.html. Source/delivery hashes are in sha256.json. Original metadata and source images are retained under source/.
