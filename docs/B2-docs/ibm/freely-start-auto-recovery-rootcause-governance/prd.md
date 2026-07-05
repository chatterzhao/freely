# PRD: freely-start-auto-recovery-rootcause-governance

## 功能要求

### 核心合同

`freely start` 在真实坏号或坏工具上失败后，必须自动把恢复链跑完，且恢复交接是单一、串行、可判定的控制面交接：

1. `freely start` 启动当前工具/当前号一次
2. 如果运行成功，继续做任务
3. 如果运行失败：
   - 先走当前工具的 slot 内循环
   - 当前工具没有更多 slot，或当前工具本来就没有 slot，可直接进入工具外循环
   - 再按工具优先级排除自己切到下一个工具，继续运行
4. 只有所有工具都不可用时，才允许进入 waiting / 停止
5. `freely stop` 必须能把整条 control-plane 干净停掉，不允许 stop 后又被恢复链反向拉起

### 输入约束

- 只改 after-failure recovery handoff 的串行化和判定合同
- 不改工具选择顺序、slot 选择顺序或 failure label 分类
- 不引入新的后台空转、重复 supervisor、或 `freely stop` 后又被抢回来的竞态

### 输出约束

- 恢复链必须串行化：old supervisor 完全退出前，不允许新 supervisor 启动同一坏号
- operator stop 必须生效：`freely stop` 后不允许再出现被 watchdog / recheck 抢回来的新 supervisor
- 恢复链必须持续：从 one-shot recheck 改成持续 watchdog 接力

## 技术设计

### 真源改动

1. `cleanup_supervisor()` 先读取共享 runtime 真相，而不是只信当前进程内的 stale `DESIRED_RUNTIME_STATE_VALUE`
2. 若已经有 replacement supervisor 存活，旧 supervisor cleanup 直接退出，不再覆盖共享 state，也不再去杀/重拉共享 control-plane
3. manager 失败后的续跑执行者，从 one-shot `launch_manager_control_plane_recheck()` 改成持续 `launch_manager_watchdog()`

对应脚本：
- `docs/system/workspace/scripts/runtime/freely` 中的 `project_cleanup_runtime_intent()` 和 `cleanup_supervisor()`
- `docs/system/workspace/skills/watchdog-control-plane/scripts/availability-watchdog.sh` 中的 watchdog 恢复接力

### 不改动的既有设计

- 工具外循环 + slot 内循环的总体合同
- worker runtime 本地 same-tool slot recovery 的方向
- 真实日志/真实 `codex exec` 作为坏号 truth 的原则
- `tool_auto_switch_selected` / availability hint 这类恢复观测面

##验收标准

### 回归验收

1. `freely start` 在当前工具先失败、fallback 工具稍后才变可用时，watchdog 会持续接力直到恢复成功
2. worker runtime 在 same-tool slot recovery 失败后能继续进入 cross-tool fallback
3. watchdog 接受实际活跃 slot 作为成功证据，即使 switch JSON 为空
4. active supervisor 失败后 control-plane 不会重复抢启同一坏号
5. `freely stop` 不会在 cleanup/recheck race 下被反向拉起
6. same-tool slot exhaustion 后能继续进入 cross-tool fallback

### 真实环境验收

1. 手工把 Codex 切到真实坏号，例如 `apikey-codex-a1016-1`
2. 执行真实 `freely start --project <project>`
3. 首轮失败后，不需要人工执行 `freely ensure-manager`
4. 系统会自动继续恢复，直到切到可用工具/号并重新运行
5. 同一次恢复过程中，不允许重复重启到刚失败的同一坏号
6. `freely stop --project <project>` 后，不允许再出现被 watchdog / recheck 抢回来的新 supervisor

### 不验收的内容

- Codex probe `hi` 成功形状规则本身（已有独立 issue）
- 旧 intake / continuity 噪音治理（不在本 scope）
- 泛化到所有 unrelated runtime bug（不在本 scope）
- root `develop` 的 daemon startup blocker（不是同一个 bug）

## 边界与依赖

### Scope 边界

只收敛这条问题：
- `freely start` 在真实坏号或坏工具上失败后的恢复交接合同

不在本条 issue 里扩展：
- Codex probe `hi` 成功形状规则本身
- 旧 intake / continuity 噪音治理
- 泛化到所有 unrelated runtime bug

### 依赖

- 无前置依赖：可直接基于 `develop` 开发
- 无阻塞依赖：不依赖其他未合并父分支

### Follow-on

- 本 issue 是 `I-20260410-1835-B`（codex-real-exec-switch-and-after-failure-recovery-governance）的 follow-on，但这次收敛的是根因修复，不是能力扩展