# Brainstorms: raw-20261107T133328Z

## 问题

「人类评论是否都标记了 resolution」这条规则有两份实现：

- `quality/comment-resolution-scan.py`（`pr-create-guarded` Step 2e 用）；
- `worktree/wt-close:450-463` 自己 `grep -c "^### comment-"` / `"^#### resolution-"`。

两份都只看行首计数，不区分系统事件评论（`- source: system`）。于是 `promote` / `promote_finalize` 写入的机器评论被当成人类评论：

- 要求补 `#### resolution-`；补了又会给本地文档增加「平台没有的块」，反而让 `raw_reconciliation` 的副本一致性不通过 —— 形成闭环矛盾；
- R13 真机：`pr-create-guarded` 先被这条卡住（已在本轮修好 scan），PR 合并后 `wt-close` 又被它自己那份旧实现卡住，且报错文案本身坏了（`$_((_unresolved - _resolved))` 打印成字面量）。

## 证据（本机实测）

- `freely wt-close --raw-key 20261104T082556Z`（R13 已合并 `42fb5833a`）输出：
  `[wt-close] raw-20261104T082556Z: 1 comments, 0 resolutions — ((_unresolved - _resolved)) unresolved` 并 `exit 1`。
- 同一文件的 `comment-resolution-scan.py` 在 R13 修复后返回 rc=0（系统评论不计）。
- 两个门禁对同一文件给出相反结论 —— 这就是「两份实现」的直接后果。

## 证伪（未被现有 open issue 覆盖）

- #4183（R13）改的是文档解析与 promote 链路；评论判定未在其验收范围内。
- #4221 之外的 open issue 无一提及 `wt-close` 的评论检查。
- 不是 #4151（测试证据链）也不是 #4075（gate failure followthrough）—— 那两条是证据内容与失败回流。

## 关键设计

1. **删掉第二份实现**：`wt-close` 改为调用 `quality/comment-resolution-scan.py`（对整个 `docs/B1-docs` 扫一遍，只对本 issue 的命中行报错）。
2. **单一真源再前进一步**：系统事件评论的识别（`- source: system`）只在 scan 里定义一次，两个门禁共用。
3. **失败要可读**：直接透出 scan 的统计行，不再自己拼 `$(( ))`。

## 被否决的替代方案

- 在 wt-close 里也加一份「忽略 `- source: system`」的判断：仍是两份实现，下次再漂移。
- 让 `promote_finalize` 同时写 `#### resolution-`：伪造人类决议，且会破坏副本一致性。
- 对 `wt-close` 用 `--force` 绕过：`--force` 会永久丢弃实现，属于明确的禁止项。
