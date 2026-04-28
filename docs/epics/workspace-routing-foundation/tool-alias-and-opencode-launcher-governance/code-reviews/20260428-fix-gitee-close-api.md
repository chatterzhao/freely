# Fix gitee-issue.py close and update API paths - verification
- issue_id: `I-20260426-0000-A`
## Implementation Decision Note
- decision: `Fix close_parser type=int→str (Gitee IDs are I-format), cmd_close and cmd_update use repo_path_post (repo in body, not URL).`
- why_this: `Gitee PATCH uses /repos/{owner}/issues/{number} with repo in body, not /repos/{owner}/{repo}/issues/{number}. The type=int rejected all 161 I-format IDs.`
- alternatives_considered: `None — this is a straightforward API bugfix.`
- boundary_non_goals: `No change to GET operations (repo_path remains for list/get).`
- residual_risk: `None — all 161 issues verified closed via direct API.`

## Verification
- Gitee close IJFOAK (string ID): `pass`
- 161/161 issues closed via direct API: `pass`
- cmd_close now uses repo_path_post: `pass`
- cmd_update now uses repo_path_post: `pass`
