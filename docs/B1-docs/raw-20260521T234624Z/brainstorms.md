# Brainstorm
## Root Cause
execution_network_transient with opencode → no auto-recovery → supervisor exit → ERR trap recurses.
The crash report always showed "bash at freely:19074" because the 2nd ERR invocation hit the function definition.
## Fix
set +e + re-entry guard in _on_supervisor_err prevents recursive ERR trap.
