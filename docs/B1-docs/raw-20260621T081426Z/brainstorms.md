# B1_IBM: complete intake migration

## Discovery
Chat→Manager pathway broken: messages written to docs/issues/ but Manager reads from deprecated .freely/intake/. Handler hardcodes old paths.

## Research
Three gaps: Manager prompt reads wrong source, handler rejects raw-* ids, no stale cleanup for consumed chats.

## Decision
Fix all three: add friedly.db reader to Manager prompt, update handler for docs/issues/ paths, add 7-day stale marking.
