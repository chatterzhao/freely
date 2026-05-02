# Tasks: runtime-audio-notifier-and-sound-semantics-governance

1. Materialize `AudioCueRequested` as a canonical runtime event.
2. Freeze first-round sound semantics for `manager|worker × started|completed`.
3. Keep notifier boundary independent from watchdog / recovery supervision.
4. Add bundled audio assets for the four standard cues.
5. Add a frontend-only audio notifier hook that subscribes directly to the event-capable adapter.
6. Keep snapshot refresh and human-readable event rendering separate from playback logic.
7. Add focused Rust and frontend regressions for event payload shape, routing, and playback dispatch.
