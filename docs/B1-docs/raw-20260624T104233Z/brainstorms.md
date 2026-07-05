---
b1_id: B1-20260624T104233Z
phase_state: completed
source_raw: raw-20260624T104229Z33Z
source_url: https://github.com/chatterzhao/freely/issues/3427
produced_candidate: C-20260624T104233Z-A
created_at: 2026-06-24
---

# B1_IBM: 全项目搜索 stop/start daemon 等测试硬编码，改为指向 pre-tests.md

## Input
- GitHub issue: #3427
- RAW key: 20260624T104233Z
- Previous fix: raw-20260624T081358Z58Z (issue #3411) — 已修 SKILL.md 和 AGENTS.md
- 当前问题：AGENTS.md 中仍保留硬编码的 numbered steps（pre-init-runtime、freely-package、start daemon、verify Manager cycle）

## Problem
项目中多处仍写 "stop/start daemon" 作为测试方式，未指向 pre-tests.md。之前改了 SKILL.md（freely-fix-execution、freely-test-execution、freely-feat-execution）和 AGENTS.md，但 AGENTS.md 的 numbered list 仍有残留硬编码步骤。

Freely 面向任意类型项目（CLI 工具、库、配置项目等），测试方式应由 pre-tests.md 定义，不能由 AGENTS.md 硬编码。

## Discovery
- 全项目搜索确认：三个 skill 文件已全部指向 pre-tests.md，无 daemon 硬编码
- AGENTS.md 自举示例已标注为 "（daemon 型项目参考）"
- bin/wt-create、bin/test-pre-merge-selfhost 等脚本无测试硬编码问题
- AGENTS.md 的 numbered steps（1-5）是唯一残留，但它们属于自举示例的上下文

## Decision: 替换 AGENTS.md 中 hardcoded steps 为 pre-tests.md 委托

1. 保持 "验证方式由 pre-tests.md 中的测试用例决定" 作为第一句
2. 删除 numbered steps 1-5（硬编码 pre-init-runtime / freely-package / start daemon / verify Manager cycle）
3. 保持 Freely 自举上下文和 `./bin/test-pre-merge-selfhost` 引用
4. 自举示例标注为 "Freely 自举端到端门禁（daemon 型项目参考）"，符合 issue 的排除规则

## Candidate
- candidate_id: C-20260624T104233Z-A
- status: promoted
- milestone: M-20260624T104233Z-A
