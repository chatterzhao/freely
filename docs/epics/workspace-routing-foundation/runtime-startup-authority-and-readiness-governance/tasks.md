# Tasks - runtime-startup-authority-and-readiness-governance

1. Introduce a runtime-owned current-launch identity or equivalent startup-truth artifact.
2. Hold the project start critical section until current-launch startup truth is durably published.
3. Rework attach-or-wait-or-repair and daemon-ready checks to consume current-launch truth.
4. Prevent fake or ghost supervisors from validating as authoritative runtime ownership.
5. Align stop cleanup and stop-marker retention with validated launch ownership.
6. Add focused regressions plus one real-repo-shaped replay for closeout.
