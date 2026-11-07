# Brainstorms: raw-20261103T132540Z

## 问题

合并门禁把「评审产物文件存在」当成「评审通过」，从不打开文件解析 verdict；评审侧又把「无法判定」默认成 pass。两层叠加后，「通过」不携带任何信息：

- `docs/system/workspace/scripts/worktree/pr-merge-guarded:622-629`（修改前）：`_review_file` 非空即 `echo "[MERGE-GUARD] PR review: pass ✓"`。
- `bin/pr-review-guarded:329-339`（修改前）：`_review_verdict="pass"` 是默认值，只有 `freely-review` 退出码非 0 或输出命中 `verdict.*fail` 才改判；`needs_changes`、超时、空输出全部落 pass。
- 结论还可被 `--verdict pass --reason <任意文本>` 显式覆盖，且 reason 完全不落盘。
- `governance-merge-gate`（修改前 `1763-1766`）对 `phase == "completed"` 直接 `continue`，跳过 `verification_artifact_dir` 与 owner review 要求；而 `bin/pr-review-guarded:711` 评审通过后把 `done_b2_ibm` 改成 `completed` → **「审查过」这件事本身关闭了「必须有审查产物」的开关**。

## 影响

review 文件写 `verdict: fail` 也照合并；作者一句 `--verdict pass --reason "急"` 可自放行；`completed` 豁免让治理门在评审通过后失效。合并门禁对 develop 的全部强制力都建立在一个恒为真的判断上。

## 证据

- 格式普查：`docs/B2-docs` 下 401 份 `pr-review-*.md`，其中 399 份含 `verdict:` 行（AT-001 census 实测 `402 review docs, 400 with verdict, 0 unparseable（含本轮新增 1 份；合并前基线 401/399）`）。
- 历史写法并存：`- verdict: pass`（多数）与 `- verdict: **pass**`（本会话 R1..R9.5 共 9 份粗体），另有 3 份历史 `fail`。
- 因此任何只看单一写法的解析器都会对历史语料自我锁死 —— 这是本 issue 的设计硬约束，不是附带细节。

## 证伪（确认为未被覆盖的独立缺陷）

拉取双平台 open issue 清单后逐条比对：#4146（R8，shim fail-open）只覆盖 `.githooks/` 的 `-x`/`-f` 与 `exit 2`；#4147（R9，commit-msg 接线）只覆盖提交期 trailer/handshake；#4151 是测试证据链与 CI 执行。三者都不涉及「读 verdict 而非查文件」，故本 issue 需要独立完成，且依赖 R8 已完成（否则门禁本身不可信）。

## 关键设计

1. **单一 verdict 真源**：新增 `review_verdict.py`（解析）+ `review-verdict.sh`（bash wrapper，导出 `freely_parse_review_verdict` / `freely_review_verdict_check`），读侧 `pr-merge-guarded`、写侧 `bin/pr-review-guarded`、审计侧 `governance-merge-gate` 全部共用，不再产生第二份正则。
2. **只认 `pass`**：`fail` / `needs_changes` / 缺失 / 无法解析一律 fail-closed；解析器剥离 `**`、反引号与引号，兼容历史两种写法。
3. **默认值反转**：`pr-review-guarded` 的「无法判定」从 `pass` 改为 `needs_changes`；`--verdict` 覆盖必须带 `--reason`，只接受三个契约值，并把 reason 落痕进 review 文档。
4. **`completed` 豁免只保留记账部分**：仍不强制 `verification_artifact_dir`（历史遗留大量缺失），但必须有与该 issue 绑定、且声明 `verdict=pass` 的评审产物；显式 `fail`/`needs_changes` 不能被 `completed` 翻盘。

## 被否决的替代方案

- 在 `pr-merge-guarded` 里内联一份正则（制造第二份副本，与 #4154 契约收口方向相反）。
- 只认 `- verdict:` 列表写法（会漏掉 1 份 frontmatter 裸键历史文档）。
- 保留 `--verdict` 无 reason 覆盖（正是被利用的洞）。
- 让 `completed` 完全套用未完成分支的全部要求（`verification_artifact_dir` 在历史语料里大量缺失，会立刻自锁每轮合并）。
- 夹带修 #4149（写通道）或 #4151（测试证据链）：均超出本 issue 范围。

## 自举评审

本 issue 属于 Wave 1 可信度根基簇，与 R8（fail-open）、R9（提交期阻断）、R9.5（post-merge audit）构成同一条证据链。本轮未发现「现有 open issue 未覆盖」的新缺陷，未重复立项。
