# Implementation Decision: runtime-audio-notifier-and-sound-semantics-governance

- issue_id: `I-20260405-1215-A`
- issue_path: `docs/B2-docs/runtime/runtime-audio-notifier-and-sound-semantics-governance/issues/runtime-audio-notifier-and-sound-semantics-governance.md`

## Implementation Decision Note

- decision: `Freeze the first standard audio path as canonical AudioCueRequested events emitted by the Tauri bridge and consumed by a frontend-native notifier with bundled audio assets.`
- why_this:
  - `watchdog` already owns supervision and recovery evidence; making it play sound would widen owner scope and re-couple supervision with presentation.
  - The existing Tauri bridge already provides a stable event plane. Adding one more canonical event keeps native/tool notices and future bounded evidence adapters on the same path.
  - Bundled frontend audio assets avoid OS-specific player commands while remaining portable across macOS / Linux / Windows Tauri hosts.
- alternatives_considered:
  - `watchdog directly invokes OS audio commands`: rejected because it mixes supervision with notifier concerns and immediately creates per-OS fallback branching.
  - `session transcript / natural-language grep listener`: rejected because it is noisy, tool-specific, and weaker than native event or notice surfaces.
  - `OS resource-only path first`: rejected for this round because frontend-bundled assets are enough for the standard path and keep browser/mock + Tauri host behavior aligned.
- boundary_non_goals:
  - No fallback player implementation
  - No blocked / failed / interruption matrix
  - No cross-tool notice audit beyond recording Codex native notice as a future source family
- residual_risk:
  - Current probe command model is still a reduced runtime proxy, so some actor/lifecycle cues are inferred from present bridge state rather than a full production orchestration graph.
  - Browser autoplay rules can reject playback until the host has a user gesture; this round records the clean standard path but does not add fallback behavior.
