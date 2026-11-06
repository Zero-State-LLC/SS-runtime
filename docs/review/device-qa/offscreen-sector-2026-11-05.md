# The offscreen sector

Read 2026-11-05 from `AudioProjector.sector` on `ef68565`. No speaker was moved.

The four-letter heading stays in [facing-direction-2026-11-04.md](facing-direction-2026-11-04.md). `atan2Milli` stays in [millidegree-2026-11-04.md](millidegree-2026-11-04.md). The shipped view stays in [camera-follow-2026-11-03.md](camera-follow-2026-11-03.md). The voice cap stays in [effect-voice-ceiling-2026-11-03.md](effect-voice-ceiling-2026-11-03.md).

A missing source returns nil. The deltas are `unitsTruncated`. A source whose absolute x delta is at most half `baselineWorldWidth`, and whose absolute y delta is at most half `baselineWorldHeight`, returns nil. Past either half, the sector is `MilliDeg.normalize` of `Cordic.atan2Milli(y:dy, x:dx)`, divided by 45,000. `normalize` stays inside 0 through 359,999, so the quotient is 0 through 7.

After the cues are appended, each candidate stores the next sequence number, starting from 0, and the counter advances. A cue whose `sourceEntityId` is set then stores this sector.

This does not add a speaker.
