# Tasks - runtime-startup-authority-and-readiness-governance

1. Add runtime-owned supervisor identity truth under project run state.
2. Make supervisor validation and supervisor lookup consume authoritative identity truth.
3. Publish startup truth before releasing the same-project start lock.
4. Gate daemon ready semantics on published startup truth.
5. Align stop followthrough and stop-marker preservation with authoritative supervisors.
6. Add focused regressions for fake-supervisor rejection and daemon-ready truth, and update adjacent stop/shared-status regressions to the new contract.
