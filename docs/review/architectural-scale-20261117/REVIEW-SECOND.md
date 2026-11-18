# Second technical inspection: context face-normal convention

November17,2026 01:29UTC. Actual `comparison-z100.png` after the UV correction now shows the retained paving relationships, but residential roofs appear as empty boxes. This is a distinct adapter defect, not a failed UV correction or a new aesthetic design.

The new source renderer recomputed all normals from vertex winding. Context geometry declares face normals explicitly, and its original renderer `docs/review/building-perspective-detail-20261116/context/replay.py:57-58` uses those normals for culling. For example, residential `masonry-shell/roof/world-tile-0-0` declares `[0,0,1]` even though its ordered vertices produce a negative-Z cross product. The generic adapter culled those roof faces. Kiosk geometry uses winding-derived normals and needs that existing convention retained separately.

Required correction: preserve this intermediate renderer/output, honor explicit context normals where present and derive normals only where absent. Keep all proposed/current geometry and dimension values identical. Add visible roof-interior pixel checks and all-context explicit-normal regression, then review actual images again. No aesthetic variation, texture pass, native execution or old-source mutation.

Initial browser check at01:29 found all8images loaded and correct2112x978raw scene dimensions, same542x250.9765625CSS display sizes, full benchmark1672x941with contain, and no horizontal overflow. That check proves only image availability/layout for this intermediate, not a valid final architectural render. Jev401 required direct browser fallback. An initial eval without explicit return producedundefined, corrected by returning the metrics object.
