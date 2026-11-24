---
b1_id: B1-20261124T054201Z
phase_state: completed
source_raw: raw-20261124T054201Z
source_url: https://github.com/chatterzhao/freely/issues/4670
produced_candidate: C-20261124T054201Z-A
created_at: 2026-11-24
---

# B1_IBM: test-all 失败诊断

## 0. 设计意图审计（先于方案）

- 外部锚点（引用原文）:
  - `bin/test-all:2-4`「Aggregate test runner … Runs the verified subset (never the whole 500+ corpus at once — that would be permanently red) and prints an explicit known-broken / not-yet-onboarded list.」
  - `CONSTITUTION.md:39`「`develop` 是功能交付的默认目标分支；进入 develop 前必须满足要求的 TEST、评审与进度/恢复证据。」
  - 实测 CI run 43827151395 / 45346477702：verify job 只打印 `[FAIL] name (rc=1)` 与 `SUMMARY: 41/42 ok, 2 failed`，无断言细节；同一 tree sha 本地 43/44 全绿，AI 无法从 CI 输出定位平台层差异。
  - 相邻 issue raw-20261124T054145Z（#4669）的 AT 接入过程也反复遇到「test-all 吞输出，只能单独重跑测试看断言」。
- 判定: **实现缺陷**（设计正确）。test-all 有意跑筛选子集 + 打印 known-broken 清单的设计是对的；缺陷在执行时把每个测试的 stdout/stderr 全部 `>/dev/null 2>&1` 丢弃，使失败不可诊断。
- 与既有断言的冲突: 无。SUMMARY 行格式与 known-broken 清单是下游门禁依赖，必须保持。
- 影响面: `bin/test-all` 执行循环；CI 日志；下游依赖 SUMMARY 行的门禁（test-gate / pretests-gate / AT 的 SUMMARY 解析）。

## 0.1 全局适配反思（四问）

- Q1 类别: 流程能力（CI 失败可诊断性），非文档/治理元数据。
- Q2 职责边界: test-all 负责执行测试并报告结果；失败断言的诊断信息属于测试结果的一部分，应由 runner 保留，不该靠人工重跑。
- Q3 结构性冲突: 按字面「所有测试永远打印完整输出」会让成功的 CI 日志爆炸（45 个测试全打印）→ 反设计；正确定义是「成功只摘要、失败留诊断」。
- Q4 门禁失配: 门禁测的是 SUMMARY rc 与证据链，不测诊断信息质量；本轮新增 AT 覆盖诊断行为，不动既有门禁判据。

## Input / Problem
`bin/test-all:147/149`：`python3 "$path" >/dev/null 2>&1 || rc=$?` / `bash "$path" >/dev/null 2>&1 || rc=$?`。stdout/stderr 全丢弃。CI 失败只显示 `[FAIL] name (rc=1)`，AI 只能盲改或人工重跑，损害自举闭环（项目目标：AI 自主发现→修复→验证）。

## Brainstorm

### Option A: 失败时把该测试的完整输出直接打到 stdout
- 优点：改动最小，立即可见。
- 缺点：多个失败时日志混杂；无独立证据文件；"完整输出"可能很大。否决（不够结构化）。

### Option B: 每个测试输出到独立日志，成功丢弃、失败打印尾部并保留 artifact
- 优点：成功日志干净（SUMMARY 不变），失败有完整日志 + artifact 可上传；符合 AI 自愈需求。
- 缺点：需管理临时日志目录。采用。

### Option C: 外部包装（CI upload-artifact step）
- 优点：不动 test-all。
- 缺点：本地运行仍无诊断；治标不治本。否决。

## Decision: Option B
失败测试保留完整 stdout/stderr 到日志，打印关键错误尾部；SUMMARY 行格式与退出码语义不变；日志路径可预测便于 CI 上传。

## Candidate
- candidate_id: C-20261124T054201Z-A
- status: promoted
- milestone: M-20261124T054201Z-A
