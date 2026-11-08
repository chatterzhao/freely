---
candidate_id: C-20261105T121046Z-A
status: promoted
source_raw: raw-20261105T121046Z
created_at: 2026-11-08
milestone: M-20261105T121046Z-A
---

# Candidates

被否决的替代方案（只打印提示 / 每次调用都打包 / 直接软链项目树 / 无条件清空安装目录）见 brainstorms.md。

## C-20261105T121046Z-A: 安装态版本可证明且与 develop 同步

- candidate_format_version: v2
- title: 新增安装态一致性检查（doctor 承载）+ 打包写 hash 清单 + 原子 activate + 合并后受控重新打包
- status: promoted
- decision_reason: 实测 `latest` 的 `FREELY_PACKAGED_FROM=444985f50` 已落后于 develop `c1949aa24`，没有任何机制发现或修复；从安装态启动会静默执行旧版 runtime/门禁，修复过的缺陷在新会话「复活」。
- next_action: 建 AT-001（静态 + 隔离 FREELY_HOME 行为：落后版本 / 悬空 latest / 悬空链接 / 打包激活后一致 / 切换失败回滚 / 幂等），改 `freely-package`、`pr-merge-guarded` followthrough、`cmd_doctor`，新增 `install-state-check.py`。
- revisit_trigger: 若引入正式 release 通道或把打包产物做成可下载制品，`--activate` 的原子切换语义需与发布流程重新对齐。
- acceptance_criteria:
  - RED：`latest` 指向落后版本时检查退出非零且输出指出落后；悬空 `latest` / 悬空 `~/.local/bin/freely` 被报告。
  - GREEN：从当前 develop 打包并 activate 后检查退出 0，PATH 解析到的命令与真源代码一致。
  - GREEN：切换失败时旧版本仍可用，`latest` 与链接都不悬空、不指向已删除版本。
  - GREEN：合并 develop 后的打包触发幂等，重复执行无副作用。
  - 所有行为测试使用隔离 `FREELY_HOME`，不触碰真实安装目录。
- promotion_gate: AT-001 RED → GREEN + 回归基线对比 + governance gate
- open_questions: []
- acceptance_reviews:
  - reviewer: session-self
  - mode: desk-research + executable-reproduction
  - summary: 实测安装态落后一个 merge；逐行核对 `freely-package` / `pr-merge-guarded` / `cmd_doctor` / `FREELY_HOME`；证伪 #4192/#4205/#4198/#4151/#4187 覆盖范围。
  - verdict: pass
- promoted_issue_id: I-20261105T121046Z-A
- promoted_issue_path: docs/B2-docs/gate/platform/raw-20261105T121046Z/issues/I-20261105T121046Z-A.md
- milestone: M-20261105T121046Z-A
- session_refs: []
