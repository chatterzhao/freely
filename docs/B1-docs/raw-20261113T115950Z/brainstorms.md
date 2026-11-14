# B1 Brainstorm — raw-20261113T115950Z

## 1. 问题

R33.14 把 **L0 项目意图一致性** 写进了 `freely-tdd-review/SKILL.md`，但评审的**执行入口**没有同步：

1. ACP reviewer prompt 仍写 `Follow skill:freely-tdd-review (TDD four-question review)`，要求的 JSON 只有 `red / green / adequacy / refactor`，**没有 L0 / intent / drift 维度**。
2. 人工回退提示的步骤 3 仍是「每级检查：下层是否忠实消化了上层？」——没有 L0。
3. 后果：reviewer 只要跑完四层就能给 `verdict: pass`，L0 规则形同虚设；R33.8–R33.10 那类「四层全绿但整体漂移」仍可通过。

## 2. 设计意图（已读源码核实）

- `freely-tdd-review/SKILL.md`：L0 先于四层，L0 不过即 fail；四层自洽不能替代项目一致。
- `pr-review-guarded` 是评审唯一执行入口（ACP 与人工回退都走它），引导必须与 skill 一致。
- `review_verdict.py` 是 verdict 唯一解析器，**只读第一处 `verdict:` 行**；不校验维度集合 → 新增维度安全，但不能改 verdict 语义。

## 3. 方案

| 方案 | 做法 | 评价 |
|---|---|---|
| A | prompt 增加 L0 段 + 新增 `intent` 维度；人工回退步骤改为「先 L0 再四层」 | 与 skill 一致，不改解析器 ✅ |
| B | 只改 prompt，人工回退不动 | 人工路径仍会漏 L0 |
| C | 让 `review_verdict.py` 强校验 L0 段存在 | 变成「补字段就过」，且改门禁契约，风险大 |
| D | 只改人工提示 | ACP 主路径仍漏 |

采用 A：只改引导文本（prompt + 人工步骤），不碰 `review_verdict.py`、不碰 `pr-merge-guarded`。

## 4. 证伪

- 「skill 已写，reviewer 会自己看」→ 否：prompt 只点名四问与四维 JSON，reviewer 按 prompt 执行。
- 「加 `intent` 维度会破坏 verdict 契约」→ 否：解析器只读顶层 `verdict` 行；AT 里显式断言解析行为不变。
- 「强校验 L0 段更硬」→ 否：会被「补一段空 L0」绕过，L0 的价值是引用外部锚点原文，不是字段存在。

## 5. 边界

- 不改 L0 的五项内容与失败判据（R33.14 已定）；
- 不改 `review_verdict.py` / `pr-merge-guarded` 的判定逻辑；
- 不放宽任何门禁；不把 L0 做成可补字段通过的门禁。
