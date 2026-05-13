# Brainstorm: increase restart storm threshold

Normal daemon startup spawns 8+ processes. RESTART_STORM_COUNT=4 always
triggers false positive. Increase to 10.
