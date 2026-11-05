# Clip playback

Read 2026-11-04 from `SpriteLibrary` and `WorldRenderer.playClip` on `e4ff026`. No frame count was changed.

The tick index stays in [clip-frame-clock-2026-11-04.md](clip-frame-clock-2026-11-04.md). The anchor numbers stay in the sprite-bounds notes. The unbacked silhouette stays in [world-shapes-2026-11-03.md](world-shapes-2026-11-03.md).

A loaded texture uses nearest filtering. An unbacked clip returns false, and the caller draws the blockout. A reaction occurrence clears the sprite's actions and sets the texture for the elapsed ticks. Reduced motion, on that occurrence, uses the last frame of that clip.

Any other clip stores a token of the clip id and the direction. A changed token clears the actions, sets the first texture, and runs the animation. An unchanged token leaves that action running. A looping clip repeats the sequence. Any other clip runs it once. One authored hold uses a single animation. Mixed holds are a sequence of one-frame animations.

This does not change a frame count.
