---
raw_id: raw-20261109T085539Z
status: brainstormed
created_at: 2026-11-10
---

# Brainstorms

## 覆盖域（issue 3 条修复面）

| # | 面 | develop 实测 | 本轮 |
|---|---|---|---|
| 1 | 状态文件 `source` 可执行化 | 20 处读、15 处写，需协议迁移 + 兼容期 | ➡ 拆 **#4252 / IKU9MB**（`raw-20261110T060553Z`） |
| 2 | TSV 传 AI prompt | `consume_worker_tasks.py:23-26` 只替 `\n\r`、输出 TSV、`except: pass`；`freely:14134` 按 tab 切分 | ✅ 修 |
| 3 | 剩余 `python3 -c` 拼接 | 实测 runtime+bin 154 处；lint 全仓 108 个候选 | ✅ 加 lint 基线（不机械替换） |

## scope 收敛（沿用 R22 先例）

R22 的 4 面只做 2 面、拆出本 issue，理由同样是「协议迁移与行为不变改动不能混在一个 PR」。本轮做 2 + 3：

- 面 2 是**单点、可端到端验证**：发射侧一个 Python 文件 + 消费侧一个 while 循环，改完能证明 tab/换行/引号逐字节保留。
- 面 3 的正确交付物是「禁止新增的边界 + 可计数基线」，不是一次改完 154 处。R22 brainstorms 已指出：机械替换会破坏需要插值的合法场景（108 个候选里大量是 `${project}/docs/...` 这类内部路径）。
- 面 1 要同时改 20 处读与 15 处写，且必须给旧格式兼容读取期，否则滚动升级会丢 daemon 恢复信息；单独立项。

## 方案方向

- 发射侧：`consume_worker_tasks.py` 改 **JSON Lines**（`json.dumps` 紧凑单行），畸形行报 stderr + 计数后跳过，删除 `except: pass`。
- 解码侧：新增 `decode_worker_tasks.py`，把每条 JSON 记录输出为 **NUL 分隔的 6 字段流**。NUL 是唯一既不会出现在 JSON 字符串值里、也能被 bash `read -r -d ''` 安全消费的分隔符；AI 文本不进任何 shell 语法。
- 消费侧：`freely` 的派发循环从 `while IFS=$'\t' read -r` 改为 6 次 `IFS= read -r -d ''`，循环体逐字不动；上游 stderr 保留在 daemon 日志，`|| true` 保留「上游不可用 == 无待派发任务」的历史语义。
- lint：`quality/python-c-boundary-lint.py` 只识别 R22 已实证可利用的形态（`python3 -c` 体内单引号字符串含 `$var`），不误报 argv/heredoc 安全形式；输出候选清单与 count 作为基线。

## fidelity 基线

- 对照组在 RED 时必须 PASS：旧 TSV 拼接确实错位、R22 argv 安全形式仍在、R22 回归测试全绿。
- 行为断言要真的构造含 `\t` / `\n` / `"` / `$HOME` 的 prompt，逐字节核对往返；畸形行必须有 stderr 报告且被跳过。
- 真机 bash 冒烟：用与 runtime 完全相同的 `read -r -d ''` 形状读 NUL 流，确认 6 字段边界与内容保留。

## 价值判定

- 不过时：TSV 与 `except: pass` 实测都在；代码块缩进含 tab 是 AI prompt 常态。
- 不重叠：#4156/R22 已修 argv 与 sed；#4239 是并发 CAS/SSE/pkill；#4157 是 watchdog/日志。
- P1：含 tab 的 prompt 让 worker 永久派不出去且原因完全误导，直接卡住自举链。

## 被否决

- **只把 `\t` 替换成空格**：会破坏 prompt 内容（代码块缩进丢失），不是修根因。
- **用 `printf %q` 转义后仍走 TSV**：跨平台转义规则不一致，读侧还需还原，复杂且易错。
- **让 bash 直接 `eval`/`source` JSON 解码结果**：等于把 AI 文本重新变成可执行 shell。
- **一次性替换 108 个 lint 候选**：需逐处判断是否有外部值，机械替换会破坏合法路径插值。
- **本轮顺带做状态文件格式迁移**：需协议兼容期，无法与「行为不变」一起验证。

## Related findings

- `IFS=$'\t'` 在 `freely` 里有 4 处，只有 1 处是 worker 派发（其余 3 处是 prompt rank / worktree 列表 / 平台状态），静态断言必须精确针对派发循环，不能一刀切。
- lint 全仓 108 个候选中大量是 `${project}/...` 内部路径，属**候选清单**而非可直接替换清单；「违规数随迁移下降」需要后续轮次逐处判定。
