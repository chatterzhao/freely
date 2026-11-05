---
b1_id: B1-20261104T082740Z
phase_state: completed
source_raw: raw-20261104T082740Z
source_url: https://github.com/chatterzhao/freely/issues/4185
produced_candidate: C-20261104T082740Z-A
created_at: 2026-11-05
---

# B1_IBM: pretests-gate 把字段值里的行内代码当成语法分隔符

## Input

- GitHub #4185 / Gitee IKSWS7，执行队列 Q1，P0（实证阻断跨分支合并：#4158 与 #4186 合并时，develop 带入的治理文档字段含反引号，两次触发 pretests-gate 误判）。
- 覆盖域：`docs/system/workspace/scripts/quality/pretests-gate` 内所有读取 `- key: value` 行的函数；`bin/pretests-gate` 是 shim，不单独修改。
- raw issue 指向 `parse_fields()` 与 `parse_scalar()` 两处。预研实测发现缺陷面更广：同一有缺陷正则在 8 处出现，且有一个 raw issue 未记录的更严重副作用。
- 兼容基线：B2 story `pretests-gate-field-parsing-compat` 下的 `raw-20260717T041435Z`（门禁字段解析引号可选化，即 #3957）已经把 `parse_issue_binding()` 改成兼容裸值 / 单引号 / 双引号 / 反引号四种写法。本次修复**必须保留**该能力，不得为了简化解析而删除。

## Problem

门禁把 pre-tests.md 与 I-* issue 中的字段值当成一个受限字符集来解析：

```
^- {key}:\s*`?([^`\n]+)`?\s*$            # parse_fields / parse_scalar / phase_state / derive_tasks_path / blocker_taxonomy / follow_on_to
^- {field}:\s*['"`]?([^'"`\n]+)['"`]?\s*$ # parse_issue_binding（#3957 已放宽字符类）
```

字符类 `[^`\n]+` / `[^'"`\n]+` 把反引号与引号视为值的**边界**，而 Markdown 文档里它们只是行内代码或引用。结果：

- `- requirement: `--output` 指向 `/` 时拒绝` 匹配失败 → `testcase_derivation_missing: missing requirement`。
- `- required_evidence: 打包产物与 `.freely_version`` 匹配失败 → `pre_tests_missing: missing 'required_evidence'`。
- 门禁把「文档作者删掉反引号」当成正确修法，于是 #4186 合并时只能做纯文案规范化；这是把工具缺陷转嫁给文档，不是修复。

## Root Cause

1. **把内容字符当分隔符**：正则试图用一个字符类描述「合法字段值」，但字段值是自由文本。行内代码、冒号、`$HOME`、中文标点都是合法内容。
2. **`\s*` 跨行吞掉下一行**：`\s` 包含换行。当字段为空（`- requirement:` 后面直接换行）时，`\s*` 会跨到下一行，`([^`\n]+)` 随后把**下一行的内容**当成当前字段的值。空值因此被伪造成「有值」，且 `parse_fields()` 会把这个假值写进字段字典。这是 raw issue 未记录的更严重缺陷：不是误报缺失，而是**静默错读**。
3. **多处各自复制同一正则**：8 处独立实现，#3957 只修了 `parse_issue_binding` 一处，其余 7 处仍是旧规则；`parse_scalar` 至今不支持单/双引号写法，造成同一份文档在不同读取路径下结论不同。
4. **空值语义不统一**：`has_blocker_taxonomy()` 用两条正则分别匹配「有值」与「空值」，`issue_is_follow_on()` 要求值非空，`parse_fields()` 则没有空值语义。任何统一动作都必须逐条保留这些差异，不能一刀切。

## Brainstorm

### Option A: 只在两处正则里把反引号从字符类中去掉

- 论据：改动最小，直接对应 raw issue 描述。
- 反证：仍有 6 处旧正则；`\s*` 跨行错读未修；单/双引号在 `parse_scalar` 仍不支持；`parse_fields` 的空值语义仍未定义。属于修表面症状，放弃。

### Option B: 抽唯一真源 `_field_line_value(text, key)`，全部 8 处复用（推荐）

- 论据：一次定义「字段值就是该行剩余的全部内容」，所有读取路径共用，消除 8 份复制；返回 `(present, value)` 二元组，让「字段不存在」与「字段存在但为空」可区分，从而逐条保留各调用方的空值语义。
- 关键设计：
  - 匹配用 `[ \t]*` 而非 `\s*`，把匹配严格限制在单行内，消除跨行吞掉下一行。
  - 只剥离**首尾成对**的引号，且内部不含同种引号时才剥离；这样 `--output` 指向 `/` 时拒绝 这类含多个行内代码段的值不会被误剥，而 `` `path` `` 这类 #3957 的整体包裹写法仍被正确剥离。
  - 保留裸值 / 单引号 / 双引号 / 反引号四种写法（#3957 兼容契约）。
- 代价：需要逐函数核对空值语义，并补一组覆盖四种引号 + 14 个字段键的回归测试。

### Option C: 改用 YAML / Markdown frontmatter 解析字段

- 论据：语义清晰，能天然处理引号与转义。
- 反证：pre-tests.md 与 I-* issue 不是合法 YAML（同一文档里重复的 `- key:` 行属于不同章节），引入解析库会改变既有文档契约，且门禁目前是纯 Python 标准库、无第三方依赖。超出本 issue 边界，放弃。

### Option D: 在门禁里对字段值做反引号预剥离

- 论据：不改正则结构。
- 反证：无法区分「值里的行内代码」与「整体包裹的反引号」，且预剥离会破坏 `actual_output` 等需要保留原文的证据字段。放弃。

## Decision: Option B

抽出 `_field_line_value()` 作为唯一真源，`phase_state()`、`parse_issue_binding()`、`derive_tasks_path()`、`parse_fields()`、`parse_scalar()`、`has_blocker_taxonomy()`、`issue_is_follow_on()` 全部改为复用它。逐条保留的既有语义：

| 调用方 | 原有语义 | 统一后保证 |
|---|---|---|
| `parse_issue_binding()` | 裸值 / 单引号 / 双引号 / 反引号四格式（#3957） | 四格式全部保留，新增支持值中含行内代码 |
| `parse_fields()` | 有值才收录 | `present and value` 才收录；空值不再吞下一行 |
| `parse_scalar()` | 只认裸值与反引号 | 扩展为四格式，不退化 |
| `has_blocker_taxonomy()` | 字段存在即算（含空值行） | 用 `present` 判定，空值行仍算存在 |
| `issue_is_follow_on()` | 值非空才算 follow-on | 用 `present and value` 判定 |
| `derive_tasks_path()` | 有值才覆盖默认路径 | 用 `present and value` 判定 |
| `phase_state()` | 取反引号包裹值 | 四格式兼容，取完整剩余行 |

不纳入本 PR 的边界：不改 pre-tests.md 的字段集合与取值枚举；不改门禁的失败分类；不改 `bin/pretests-gate` shim；不调整任何证据文件的路径约定；不修平台读通道、raw key 漂移等独立缺陷（均已有各自 raw issue）。

## Related findings (not new raw issues)

本轮跑回归时发现 `docs/system/workspace/scripts/tests/` 下 9 个 legacy 门禁测试在 **develop HEAD `b9a89fb08` 上本来就是红的**，与本 PR 无关：它们断言英文消息（例如 `missing pre_tests_path`、`not based on a specific issue`、`ephemeral verification surfaces`），而现行实现输出中文或已改写的消息。以「未修改的 gate」与「本 PR 的 gate」逐项对比，9 个测试退出码完全一致，证明零回归；新增的 AT-001 测试在基线 RED、修复后 GREEN。

该现象已被现有 open issue `#4151`（`raw-20261103T132548Z`，让测试证据链可验证并替换 CI 桩）覆盖——其正文明确写有「无聚合 runner」「519 个测试永久无人执行」「其余标 known-broken 并纳入 TODO」。按「只给现有 open issue 未涉及的缺陷新建 raw issue」的约束，**不重复创建 raw issue**；本轮的具体失败清单记入 AT-001-GREEN.log 作为该 issue 的补充证据。

## Candidate

见 `candidates.md` 的 `C-20261104T082740Z-A`。
