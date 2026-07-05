# Brainstorm: nightly version timestamp
## Context
Current format YYYYMMDD-nightly loses time granularity. Same-day rebuilds overwrite.
## Fix
Change to YYYYMMDDTHHMMZ-nightly in freely-package validation + test-pre-merge-selfhost generation.
