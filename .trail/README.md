# Trail repository context

Trail-code is used through the `trail` CLI and the graph-first instructions in
`AGENTS.md`. The `/trail` skill is available in Jcode. No automatic Jcode hook
execution is claimed by this setup.

- `learnings/`: concise verified decisions, failed approaches and evidence links.
  Commit these with the work so other machines and agents can retrieve them.
- `cache/`: ignored, local generated graph. Run `trail build` after code changes.
- `trail status`: check graph freshness and learning discovery.
- `trail ask "specific question" --source`: retrieve relevant learnings and code.
- `trail check`: advisory diff review, not a replacement for tests or visual review.

Read `docs/handoff/NEXT.md` for the current work order and authorization gates.
Save durable lessons here rather than copying transcripts or volatile CI status.
Preserve existing authorship when adding new agent-authored lessons. Do not
commit credentials, generated graph caches or unrelated local review packets.
