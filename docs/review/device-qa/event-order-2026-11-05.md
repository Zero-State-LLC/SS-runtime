# The published order

Read 2026-11-05 from `EventBuffer.publish` on `ef68565`. No event was added.

`AuthoritativeEvent` stores schema `event-001`. Init copies `type.ordinal` into `ordinal` and stores `sequence` 0. The cases run from `runStarted` to `enemyAlerted` in declaration order, and the ordinal is ten times that position, counting from 1.

`canonical` stores the schema, the tick, the ordinal, the sequence, the type's raw value, the primary and secondary ids as decimal strings or null, and the payload. It leaves out phase and insertion.

`emit` appends one event and then adds one to the insertion counter. `publish` sorts by phase, then ordinal, then primary raw with a nil id as 0, then secondary raw with a nil id as 0, then insertion. It writes `sequence` to the sorted index, clears the pending list, sets insertion back to 0, and returns that list.

This does not add an event type.
