# PRD: raw-20261127T110239Z
## Goal
平台评论失败必须给出准确、可操作的原因；已关闭 Issue 不被盲目评论；重跑不制造重复评论。
## 实现方案
`cmd-comment.sh` 评论前读 Gitee Issue 状态；`gitee-issue.py api_request()` 翻译特定 401；`cmd-promote-finalize.sh` 据 `last_synced_comment_at` 跳过重复评论。
## Dev-Loop Handoff
RED 2/9 → GREEN 11/0；unit 函数级测试覆盖三处契约。
