---
raw_id: raw-20261110T101358Z
status: brainstormed
created_at: 2026-11-10
---

# Brainstorms

## 来源与覆盖域

R23.10（#4254，派发 CAS + SSE 收敛）的真源普查中发现：`runtime/a2a_task.py` **整个模块无法加载**。这是 #4254 的前置阻塞 —— 不修就无法构造可信的派发 RED。

实测（develop `ab86c1b16`，Python 3.13.12）：

```
$ python3 docs/system/workspace/scripts/runtime/a2a_task.py list --role worker --status submitted
  File ".../a2a_task.py", line 435, in <module>
    def _sse_pool() -> SSEPool:
                       ^^^^^^^
NameError: name 'SSEPool' is not defined
```

- `:435` 用 `SSEPool` 作返回类型标注，`class SSEPool` 在 `:446` 才定义；
- 文件头无 `from __future__ import annotations`，Python 3.13 在定义时求值标注 → 导入即失败；
- 全文件只此一处前向引用标注；引入自 commit `eb03edc74`（Phase 1 SSE client）；
- `git diff develop -- a2a_task.py` 为空；**安装态** `~/.freely/versions/latest/...` 同样失败；
- `bin/test-all --ci` 全绿却没发现 —— `grep -rln a2a_task.py tests/` 只有 `test-reviewer-contract.py` 引用到文件名，**没有任何测试执行该 CLI 入口**。

## 影响

派发循环 `freely::manager_runtime_launch_workers`（约 `:14130-14310`）整条链路依赖此 CLI：

```
a2a_task.py list --role worker --status submitted 2>/dev/null
  | consume_worker_tasks.py | decode_worker_tasks.py > stream || true
```

还有 `latest-manager` / `latest-completed-worker` / `active-workers` / `insert` / `update`。模块加载失败时 `2>/dev/null` + `|| true` 双重掩盖 → 空流被当成「没有待派发任务」，**worker 派发静默停摆**，运维只看到「没有任务」看不到根因。

与 #4246 同族：那次是 `except: pass` 让畸形输入表现为「没有待派发任务」，这次是 CLI 级失败被 shell 吞掉。也印证 R27/#4165「核心 runtime 缺 TDD 证据链」，但本条只修可加载性 + 最小冒烟，不扩大 scope。

## 方案方向

### 方向 A：`from __future__ import annotations`（选中）
- 一行修复所有前向引用；运行时行为不变；不影响已定义类；Python 3.7+ 支持。
- 不碰 `:435` 的标注文本，也不挪 `SSEPool` 定义 —— 避免动 SSE 语义。

### 方向 B：把标注改成引号 `'SSEPool'`
- 也可行，但只修这一处；将来新增前向引用会再犯。方向 A 是结构性修复。

### 方向 C：把 `SSEPool` 定义上移
- 需要搬 200+ 行代码，风险与收益不成比例，且可能改变初始化顺序。

### 方向 D：改 shell 侧去掉 `|| true` / `2>/dev/null`
- 属 #4157 / R25（失败语义与可观测性）范畴，不是本条；本条只消除触发它的根因，不改容错语义。

**选 A + 把 CLI 冒烟接入 `bin/test-all` 的 `CORE` 与 `CI_CORE`**（两个列表都加，否则 CI 仍是「全绿但 CLI 起不来」）。

## 被否决

- 放宽 `test-all`、改状态机 / `--expected-status` 参数（那是 #4254）、改 SSE watchdog 实例数（#4254）、删除 `|| true`（#4157）、重写 `a2a_task.py`。

## fidelity 基线

- RED 必须复现 `NameError`，且证明 `list` / `update` 两个入口都挂；静态断言冒烟 AT 存在且接入 `bin/test-all`。
- GREEN 必须证明：模块可 import；`list` / `update` 返回**明确业务错误**（A2A Server 未启动）而非 `NameError`；`SSEPool` / `_sse_pool` / `A2AClient` 仍在（语义未变）；`bin/test-all --ci` 真的执行新冒烟。
- 2 项 RED PASS 是守卫（冒烟文件存在、`list` 在无 server 时产出错误形状），不是新功能。

## 价值判定

- 不过时：develop 与安装态实测均失败。
- 不重叠：#4254 是派发幂等 / SSE 实例；#4246 是输入边界；#4157 是可观测性；均不覆盖「模块加载即崩」。
- 高价值（P0）：整条 worker 派发链路静默停摆，且是后续所有派发相关修复的前置。
