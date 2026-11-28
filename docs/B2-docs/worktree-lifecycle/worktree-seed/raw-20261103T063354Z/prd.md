# PRD: PR 收尾平台名对齐
## Goal
消除 unknown: origin 伪错误，让收尾回执可诊断。
## 实现
- platform-adapter CLI 增 `configured-platforms` 只读 JSON 动作。
- pr-merge `_sync_prs_across_platforms` 改读该动作，过滤 github，逐平台结构化回执。
## Handoff
先 RED（baseline 仍按 remote 循环），再实现，再 GREEN。
