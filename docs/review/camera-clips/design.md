# BP-004 camera clip source proposal

Status: authored source candidate, not art admission. Implements the existing BP-004 six-clip/fixed-mount requirements. No timing, gameplay, collision, damage or Reduced Motion contract changes.

Research checked 2026-10-14:
- Apple, https://developer.apple.com/documentation/spritekit/skaction/animate%28with%3Atimeperframe%3A%29 : texture actions traverse supplied textures at a specified time per frame. Existing v1 metadata supplies the candidate frame order and cadence.
- Game Accessibility Guidelines, https://gameaccessibilityguidelines.com/avoid-flickering-images-and-repetitive-patterns/ : avoid flickering/repetitive visual effects where possible. This supports restrained effects, not a claim that specific amplitudes are tested or safe.

Authored comparison proposal: retain a single permanent pole/mount/base; small indicator-only modulation in the four operational holds; a compact local material response over already-damaged geometry for hit/critical entry; immediately dark broken geometry with a brief matte fragment fall contained near the dome for destruction. The field-off and destroyed-idle deliveries hold the same settled dark image. Identical destroyed-idle holds are intentional persistence, not falsely claimed distinct movement. Keep frame slots and durations exactly as metadata; do not invent a sweep or heading change.

The candidate's effect amplitudes, fragment coordinates and colors are authored source parameters, not research-derived constants. Reduced Motion preview selects the settled terminal state immediately. Runtime must still arbitrate newest authoritative integrity, destruction and field removal; an HTML source preview cannot prove that behavior. Runtime notch overlays stay separate. Compare native size, grayscale, normal and slowed playback before runtime capture/admission. Existing Captain distinction and legal/dense encounter requirements remain open.
