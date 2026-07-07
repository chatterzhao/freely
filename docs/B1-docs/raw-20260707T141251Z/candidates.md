---
candidate_id: C-20260707T141251Z-A
status: promoted
source_raw: raw-20260707T141251Z
milestone: M-20260707T141251Z-A
---
## C-20260707T141251Z-A: platform-adapter 改为 Handler 注册表模式
- status: promoted
- decision_reason: 新平台只需写一个 Handler 子类 + register() 一行
- promoted_issue_id: I-20260707T141251Z-A
- promoted_issue_path: docs/B2-docs/ibm/b2-governance/raw-20260707T141251Z/issues/I-20260707T141251Z-A.md
- acceptance_criteria:
  - PlatformHandler ABC 定义完整的平台接口
  - GitHubHandler + GiteeHandler 从原代码提取
  - 注册表模式: register(handler)
  - 所有公开函数遍历 registry，无 if/elif 硬编码
  - CLI 接口不变
  - 现有调用方不感知变化
  - python3 -m py_compile 通过
