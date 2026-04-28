# File size config - verification
- issue_id: `I-20260426-0000-A`
## Implementation Decision Note
- decision: `Make file size check configurable via FILE_SIZE_WARN/ERROR. Add skip markers (# file-size: skip / file_size_check: skip). Add skip markers to legacy large files.`
- why_this: `User can set own thresholds. Third-party files (skills from others) can opt out with a marker.`
- alternatives_considered: `1) Hardcoded limits: rejected, inflexible. 2) Per-file config: rejected, complex. 3) Config + markers: chosen, simple.`
- boundary_non_goals: `No enforcement at gate level (advisory only).`
- residual_risk: `Skip markers are searched with grep, may have false positives on discussion of the feature.`
