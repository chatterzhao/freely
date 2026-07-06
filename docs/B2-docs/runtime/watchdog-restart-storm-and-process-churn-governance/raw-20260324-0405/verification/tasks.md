# Tasks: watchdog-restart-storm-and-process-churn-governance

- materialize restart-storm/process-churn runtime signal helpers in `runtime/freely`
- extend `write_session_state` and status readers for churn signal fields
- keep `workcell-state.env` free of restart-storm/process-churn counters
- update watchdog flow so signal hit pauses blind relaunch and enters low-frequency observation
- wire manager escalation handoff from signal hit
- expose signal summary in `live-status` / `fleet-status`
- add runtime tests for signal emission, no-mirror, escalation, and low-frequency observation
