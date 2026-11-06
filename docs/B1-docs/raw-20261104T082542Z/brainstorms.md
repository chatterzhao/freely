# Brainstorms: raw-20261104T082542Z

## 问题

`wt-create` 经 `raw-issue-pull` → `platform-adapter.pull_raw_issue()` 物化平台 raw issue 时，落盘内容为 frontmatter + `workflow_kind` + 正文，**没有 `# <title>` 一级标题**。而：

- `raw-reconciliation-gate.py::_local_record()` 用 `re.search(r"^#\s+(.+)$", body, re.MULTILINE)` 提取本地 title，匹配不到则 `title=""`；
- `canonical_projection()` 会把平台 title 的 `[RAW-<key>] ` 前缀去掉；
- 于是本地 title 为空、平台 title 非空 → fingerprint 不一致 → 每个新 raw issue 的**首次 PR 必被 `content_diverged` 阻断**。

Q1、Q2、R1 三轮都是靠人工现场补 H1 才继续，属每轮固定成本。本轮 `wt-create` 物化的 `docs/B1-docs/raw-20261104T082542Z/issue.md` 再次实测确认无 `# ` 行。

## 规模与风险评审

- 本地 805 份 raw issue.md 中 **700 份缺 H1**（87%），其中 **410 份已 absorbed**、690 份有 GitHub issue_id、仅 6 份有 `issue_title` frontmatter。
- 另有 **18 份已含多个 H1**（历史遗留），回填若不加幂等会把它们改得更乱。
- 因此「回填 700 条」不能在本 PR 里批量执行：涉及 700 个文件、多数已终态，且标题来源不可靠。**本轮只交付默认 dry-run 的回填命令**，不改写历史语料；命令本身必须「不瞎编标题」。

## 不退化边界（Q2 刚收敛，用户明确禁止退化）

1. `canonical_raw_title()` / `is_canonical_raw_title()` / `platform_title()` 三个既有函数行为逐字节不变。
2. `_created_at_to_key()` 兼容分支保留；平台标题未声明 canonical 身份时仍做达标修正，但本地 `raw_key` / `target_dir` 不漂移。
3. `_resolve_raw_identity()` 的单条兜底保留。
4. `issue-sync._platform_title()` 的自动达标能力不受影响。
5. `feedback edit` 的标题规范化不受影响。

## 根因

`pull_raw_issue()` 落盘语句为 `f"---\n{fm_str}\n---\n\n{body}\n"`，`title` 变量只用于 raw key 校验，没有进入 payload。

## 关键设计决策

- **复用 Q2 单一真源**：在 `raw_title_contract.py` 新增纯函数 `local_heading_title(raw_key, title)`，返回「平台 canonical title 去掉 `[RAW-<key>] ` 前缀后的纯标题」，而不是在 adapter 里另写一套剥离逻辑。这样平台侧（canonical_projection 去前缀）与本地侧（_local_record 取 H1）必然对齐。
- **精确前缀剥离**：发现 Q2 的 `_STALE_PREFIX` 正则只匹配时间戳形状 key；4 个历史非标准 key（`20260501`、`20260503`、`20260503-0000`、`MIGRATED`）会产生重复前缀 `[RAW-20260501] [RAW-20260501] ...`。不改 Q2 既有函数，而是在新 helper 里先按精确 key 剥前缀再委托，既修边界又不退化。
- **幂等**：body 已有 `# ` 行时保留原 H1（包括 18 份多 H1 的历史文件），不重复注入；重复 pull 仍只有一个 H1。
- **H1 单行**：折叠空白，保证不破坏 Markdown 与 `_local_record` 的行匹配。
- **回填命令安全契约**：默认 dry-run 且 exit 0；标题只来自 `issue_title` frontmatter 或平台 replica；无可靠来源则 SKIP；已有 H1 的文件逐字节不动；`--apply` 需显式、原子写、可重复执行。

## Related findings（自举评审）

- 4 个历史非标准 raw key 暴露了 `canonical_raw_title()` 的边界（非时间戳 key 会产生重复前缀）。该缺陷在 `issue-sync` 更新这些历史 issue 的平台标题时仍可能触发，但**不在本 issue 范围**（本轮只保证新 helper 正确，不改 Q2 函数），且现有 open issue 中 #4154「契约常量与 raw key 多副本收口」与其同簇。未新建重复 raw issue；证据写入 AT-001-GREEN.log 与 review verdict 的残余风险。
- 3 个 `test-merge-guarded*` 恒 ENOENT 等预存红测试 → 已被 #4151 覆盖（R1 已记录），本轮未重复创建。

## 可行性预验证

- `git cat-file --batch` 之外的本轮关键前提：`_local_record` 的 H1 提取与 `canonical_projection` 的前缀剥离在真实平台副本上实测 **fingerprint `9140d678763e4dd9` 完全一致**，title/body 双 MATCH。
- 805 份真实 issue.md 的 Q2 既有函数新旧对比 0 差异；7 个相关回归测试全 PASS。
