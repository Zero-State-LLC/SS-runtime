# BP-002 controlled-source pilot

Specs deepened first at 679328f459b58f5027c32eb78bbc4a08f1c2a15d: controlled-character-source.md, benchmark-production, plan, tasks and acceptance. Runtime's four pin sources now adopt that commit. No production artwork, active clip version, gameplay identity or sprite renderer changed.

Research: Blender IK exposes chain targets and stretch; Spine documents weighted meshes, IK and PNG-sequence export. The spec distinguishes documented mechanisms from the proposed 3D source pilot. Official sources and retrieval limitations are in controlled-character-source.md. This is source-authoring research; no new runtime engine or license purchase.

OBSERVED local execution limitation: Blender 5.2.0 LTS printed its version, but background startup exited 139 before the Python script, with a crash in Metal GPU detection. The native application opened but its controls did not respond to the attempted automation. build.py is the local recipe, not proof of local execution; build.log records that failure.

OBSERVED hosted execution: the Higgsfield 3D editor executed remote-build.py and committed revision 1 in project e428d4b6-3697-4c74-ae65-78764240abde. Editable source is stored by the service; scene-evidence.json records revision, artifact identifiers, sizes and etags, not local SHA-256 hashes. No AI image/video generation or catalog import was used in this step.

[Editable source project](https://higgsfield.ai/3d-jutsu/e428d4b6-3697-4c74-ae65-78764240abde)

The pilot has 15 named bones, independent foot targets, two-bone leg IK with stretch disabled, a restrained pelvis compression/torso lean and a fixed orthographic technical camera. Seven evaluated samples give a maximum ankle-target residual of 1.2028708e-06 source units. Thigh length range is 0.441474947–0.441475453; shin range is 0.460977728–0.460979064. Values are numerical solver evidence, not a visual slipping tolerance. Source units and technical camera are not approved game-world mapping.

Visual inspection: 512×512 renders at frames 1, 4 and 7 were retrieved through the service and viewed in the browser. Full rig stays in frame; peak pose visibly bends knees while endpoints stay in place; final returns to rest. The displayed forms are deliberately debug bone proxies, not a body, costume, hands or character art. Only rest/peak/final renders were inspected; intermediate samples have numeric evidence only. GLB proxies carry sampled keys for inspection; they are not a skinned character and not a production export.

OPEN: anatomical and costume mesh, deformation controls, pole/joint direction robustness beyond this small response, four distinct elevated facings, benchmark materials/lighting, source-to-game registration, 16-frame world-travel cycle, hurt-to-live-state transition, runtime scene and device acceptance. The technical pilot must not replace any of those requirements or lower the art target. A fixed foot in this stationary source does not establish contact during actor travel.

Validation: specs validator passed (23 JSON, 7 schemas, 33 contracts, 55 indexed files); timing migration checker passed (59 clips, 218 facings, 14 malformed cases, 5 vectors); unchanged parity script passed against the local pinned Git object tree; 7 focused Swift contract-version/timing tests passed. No new full-core or simulator run was needed for this spec-pin/source-only change. Physical device was not used.
