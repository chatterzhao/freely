# Brainstorms: raw-20261104T082556Z

## 问题

`issue-sync promote` 把 B2 的 I-* 交给 `cmd_create` 创建平台 issue，而 `cmd_create` 只认 B1 布局：

- `cmd_promote :796` 先在 `docs/B2-docs` 里 `find` 到 I-* 文件（有），随后 `cmd_create "$i_id"`；
- `cmd_create :519` `file="$ISSUES_DIR/$local_id/issue.md"`，`ISSUES_DIR=docs/B1-docs` → 必然 `not found` 并 `exit 1`。

因此 promote 对任何 B2 目标都必然失败，`promoted_children` 永不记录，`promote-finalize`（依赖 children）跟着失败，raw 无法正常 absorbed。

## 证据（本机实测）

- R12 收口时真实执行 `freely issue-sync promote raw-20261104T082603Z I-20261104T082603Z-A`：先报 `docs/B1-docs/20261104T082603Z/issue.md not found`（缺 `raw-` 前缀，另一处解析问题），带前缀重跑后报 `docs/B1-docs/I-20261104T082603Z-A/issue.md not found` —— 即使 B2 文件存在于 `docs/B2-docs/gate/platform/raw-20261104T082603Z/issues/`。
- 同一假设在 5 个命令里重复：`cmd_create` / `cmd_update` / `cmd_comment` / `cmd_close` / `cmd_status` 全部 `file="$ISSUES_DIR/$local_id/issue.md"`。

## 证伪（未被现有 open issue 覆盖）

- #4184（R12，已合并）修的是**关闭路径顺序**与退出码，promote 路径未改。
- #4185/#4188 是 pretests 字段解析与 raw key 漂移；#4186 是 wt-create 四态恢复。
- #4154（契约常量与多副本收口）是关于常量与 raw key 副本，不是文档路径解析。

## 关键设计

1. **单一解析器** `_issue_file_for <id>`：先 B1 `docs/B1-docs/<id>/issue.md`，再 B2 `docs/B2-docs/**/issues/<id>.md`（精确名优先，历史前缀变体作兜底）；0 个 → rc 1 并列出检查过的位置；多于 1 个 → rc 2 并列出候选（fail-closed，不猜）。
2. **五个命令统一走解析器**：create / update / comment / close / status —— 同一根因只修一半会留下「update/comment 对 I-* 仍然必失败」的半修状态。
3. **`cmd_promote` 也用解析器**：删除 `find -name "${i_id}*.md"` 的模糊前缀搜索（`I-x.md` 与 `I-x-A.md` 会互相误命中）。
4. **`platform_state` 只在字段已存在时写**：它是 raw 字段，linked I-* 文档没有该键，无条件 `_fm_set_str` 会把 I-* 的 schema 改掉。新增 `_fm_has_key` 守卫。

## 被否决的替代方案

- 只改 `cmd_promote`（复制一份路径解析）：会有第二份真源，且 update/comment 对 I-* 仍失败。
- 把 B2 文档复制/软链到 B1 目录：制造两个真相源，close/batch 会读到不同副本。
- 用 `find | head -1` 取第一个匹配：ambiguous 时静默选一个，属于随机行为，不可接受。
