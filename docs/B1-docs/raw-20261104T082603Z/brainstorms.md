# Brainstorms: raw-20261104T082603Z

## 问题

`issue-sync close` 把「平台写」放在了「本地契约校验」之前，两个方向都产生不可判的结果：

1. **非终态先关平台再报错（issue 原文）**：`raw_lifecycle_effects.py:59` 的 `close_platforms()` 先调用 adapter `close-multi` 把所有平台副本关掉，**之后**才执行 `transition_issue(..., "platform_closed")`；而该事件要求 `phase_state ∈ {absorbed, dropped}`（`raw_metadata_contract.py:233`）。本地还是 `proposed` 时，平台已经 CLOSED，命令却以 `[raw-lifecycle] platform close requires terminal raw phase` + rc=1 收场 —— 平台已变、本地未变、调用方按 rc 认为「失败」。
2. **部分成功被写成「已关闭」**：非严格路径（`bin/issue-sync:745-760`）逐平台关闭，每处失败只 `echo "... close FAILED" >&2`，然后**无条件** `_fm_set_str "$file" platform_state closed`。即一个平台关失败也能拿到 `platform_state=closed` 的自证结论，重试扫描直接跳过。
3. **部分成功与全失败同码**：adapter 的 `close-multi` / `close-raw` 都是 `0 if all closed else 1`，调用方无法区分「已经关掉一半」与「一个都没关掉」。R11 已把 `create-issue` 改成 0/3/1，关闭路径没跟上。

## 证据（本机实测）

- issue 原文实测：`issue-sync close raw-20261104T074512Z` 输出 `github: closed` / `gitee: closed`，随后 `[raw-lifecycle] platform close requires terminal raw phase` 与 `[ERROR] ... close failed`，`gh issue view` 确认已是 `CLOSED`。
- 代码位置逐行核对：`raw_lifecycle_effects.py:68-78`（adapter 先、transition 后）、`raw_metadata_contract.py:233-236`（终态约束）、`bin/issue-sync:693-700`（严格路径只把非零压成 `return 1`）、`bin/issue-sync:745-760`（非严格路径无条件写 closed）、`platform-adapter.py:1475-1485`（`all closed else 1`）。
- 严格路径的 retry 语义：平台侧关闭是幂等的（`gh issue close` / `gitee close` 对已关闭对象返回成功），因此「先校验、后执行」不会破坏重跑自愈。

## 证伪（未被现有 open issue 覆盖）

- #4149（R11，已合并）只修**写原语与创建路径**，并在 `cmd_close` 两处注释里显式把关闭路径的部分成功口径留给本条 —— 未覆盖。
- #4136 / #4137 是 `pr-merge-guarded` 关闭 Gitee PR 时把远端名当平台名、`gitee-issue.py delete-branch` 路径错误，属 **PR/分支** 通道，不是 issue 关闭通道。
- #4166 是「双平台同步入口与副作用收口」，是入口层重构；本条只修关闭路径的**顺序与退出码**，不改入口分层。
- #4135（test-gate 语义）与 #4151（测试证据链）与关闭路径无关。

## 关键设计

1. **四段式契约**：`校验 → 执行 → 回写 → 退出码`。`close_platforms()` 先用纯函数 `transition(metadata, "platform_closed")` **预演**目标状态（不落盘），非终态在这里就失败，平台一个都不动。
2. **预演结果即回写内容**：校验通过后把预演得到的 metadata 暂存，平台全部关闭成功才 `write_issue()` 落盘 —— 避免「先写状态再发现平台失败」的反向自证。
3. **按平台记账**：adapter 关闭命令统一 0（全关）/3（部分）/1（全失败），并输出每平台 status；`close_platforms` 把 3 与 1 分别上抛。
4. **非严格路径同口径**：`cmd_close` 的非严格路径（I-* 等）改为「至少一个成功且有失败 → rc 3、不写 `platform_state`；全失败 → rc 1、不写」，只有全平台成功才写 `closed`。
5. **失败信息带现状**：`platform close requires terminal raw phase` 追加 `(current: <phase>, need: absorbed|dropped)`，让调用方无需回读文件即可判断该先做什么。

## 被否决的替代方案

- 只把非终态判断搬到 `cmd_close`（bash 侧）：判定规则会有第二份实现，与严格契约漂移；且 adapter 直调路径仍会重犯。
- 平台关闭失败后「回滚已关闭平台」：关闭不是可逆操作（重开 issue 会带噪音评论与状态历史），不引入伪回滚。
- 非终态时允许关闭并把退出码改 3（issue 方案 2）：仍会让「不该关的关了」，只是把不可判变成可判；本仓选择方案 1 的 fail-closed 语义。
- 顺手把 `update-issue` / `comment` 通道一并改成 0/3/1：属 #4166 入口收口，夹带会扩大回归面。
