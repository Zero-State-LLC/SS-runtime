# Native video timestamp investigation

Observed: 3,309 decoded frames have PTS matching sorted source packet PTS. 2,480 decoder-estimated timestamps differ from their frame PTS, by up to 6.88 seconds. Duplicate PTS exist; strictly increasing PTS is false. Initial boundary sheets used the estimated timestamps and therefore do not establish actual segment boundaries. Preserve those diagnostic results; do not publish exports based on them.

FFmpeg documents best_effort_timestamp as heuristic: https://ffmpeg.org/doxygen/9.0/structAVFrame.html . Its `igndts` input flag ignores DTS when PTS exists: https://ffmpeg.org/ffmpeg-formats.html . Testing that decode path against visible captions and source packet PTS is the next step. This is not authorization to invent missing frames or smooth over capture gaps.

Evidence: timestamp-diagnosis.json, packet-gaps.json and recording-gaps.json (the last uses the rejected estimated timestamps). No runtime cadence change or visual acceptance follows from this investigation.

Outcome: `+igndts` sequential decoding restored visible input/policy labels at their source PTS boundaries. All six exported Standard windows contain strictly increasing source PTS; four duplicate timestamps elsewhere in the original movie are excluded, not rewritten. Independent packet checks verify every exported frame and relative timestamp against source. See source-pts-verification.json. Recorded gaps remain in exports; no recapture or smoothing is implied.
