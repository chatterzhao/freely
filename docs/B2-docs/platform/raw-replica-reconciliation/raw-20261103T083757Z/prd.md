# PRD: raw-20261103T083757Z
## Goal
远程分支删除走 Gitee API v5 canonical 端点，避免每次 404 后 fallback。
## 实现方案
`repo_path_branch()` 返回 `/repos/{owner}/{name}/branches/{branch}`；`cmd_delete_branch` 的 DELETE/鉴权/回执语义不变。
## Dev-Loop Handoff
RED 4/4 → GREEN 8/0；不改 fallback、不改其他命令。
