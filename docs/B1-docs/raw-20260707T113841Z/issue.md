---
local_id: raw-20260707T113841Z
kind: raw
phase_state: absorbed
absorbed_into: I-20260707T113841Z-A
platform_ids:
  github:
    issue_id: '3803'
    url: https://github.com/chatterzhao/freely/issues/3803
    synced_at: ''
  gitee:
    issue_id: IJZGPL
    url: https://gitee.com/zhaoquan/freely/issues/IJZGPL
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-07-07T11:39:04Z'
updated_at: '2026-07-07T13:06:50Z'
intake_id: ''
author: platform
channel: github
session_refs: []
platform_state: closed
---

\n\n## 问题

当前 Worker agent 做完每个阶段（B1/B2/RED/dev/GREEN）后，没有强制性的独立审查。Worker 可以自己审自己、跳过审查、或糊弄审查。pr-create-guarded 没有检查 review 签名。

## 目标

建立三层审查保障：

1. **提示词层**: Agent 启动时注入阶段定义和停止信号——做完 B1 后自觉请求 review
2. **命令层（兜底）**: pr-create-guarded 检查所有 phase 的 review signature——缺失则阻塞，直接 ACP 委派 Reviewer
3. **外部裁判**: Reviewer 使用不同模型 slot，独立判定 pass/fail

## 设计决策

- **阶段指南抽象化**:  ——同一 Reviewer agent，不同阶段注入不同指南
- **节点检测**: 不靠 watchdog 扫描文件——靠命令执行时的强制检查
- **缺失委派**: 命令直接 ACP fork Reviewer（不是让遗漏了审查的 agent 去委派）
- **跨模型**: Reviewer 使用与 Worker 不同的 AI tool slot

## 实现范围

1. 创建 review-guidelines/ 目录 + 5 个阶段审查指南 (b1/b2/red/dev/green)
2. pr-create-guarded gate chain 增加 review signature 检查
3. 缺失 signature 时 → 阻塞 + ACP 委派 Reviewer
4. agent 提示词中注入阶段定义 + 停止信号说明
5. 输出格式: verdict + findings + reviewed_by

## 参考

- Routa: downstream distrust — 下游车道不信任上游产出
- Karpathy AutoResearch: 客观指标判定 — 不让 agent 决定自己是否完成
- Zed spawn_agent: 同步阻塞等结果
