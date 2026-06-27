---
issue_id: I-20260627T021849Z-A; issue_path: docs/issues/I-20260627T021849Z-A/issue.md; phase_state: done_b2_ibm
---
- issue_id: I-20260627T021849Z-A
## Implementation Decision Note
- decision: --platform-only 无本地文件时用 gh/gitee API 搜索 raw key 获取 issue 号
- why_this: --platform-only 本意就是只操作平台 API
- alternatives_considered: 强制要求本地文件(现状, bug); exit 0 跳过(不关闭 issue, 泄漏)
- residual_risk: 依赖 gh/gitee CLI 可用性，但已有的 API close 路径同样依赖
