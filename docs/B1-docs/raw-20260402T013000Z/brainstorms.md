# 研究：Backup 时间渲染与存储边界

日期：2026-04-02 01:30 UTC

## 背景

当前仓库同时存在几类时间面：

- 面向机器比较与恢复的时间真相
  - 例如 RFC3339 / ISO 字符串、epoch、日志时间、cooldown reset 时间
- 面向人阅读的显示时间
  - 例如前端 Recent Activity、CLI / watchdog 输出中的 `reset_at_human`
- 面向治理与文件系统稳定性的命名时间
  - 例如备份文件名、历史文件名、版本号、restart manifest history 名称

这三类时间面之前没有被显式分层，导致“是否应该统一改成本地时间”容易被误判成一个单一问题。

## 当前问题

### 1. 机器真相、显示时间、命名时间被混成同一层

如果把所有时间都改成“当前系统时间”：

- 机器真相会失去跨机器、跨时区和 DST 的稳定比较能力
- 文件名排序与治理规则可能被破坏
- 人类显示虽然更顺手，但会让恢复与审计链路更难比对

### 2. 当前用户感知面存在 UTC / 本地时间分裂

本轮扫描发现：

- 前端 probe Recent Activity 之前直接显示原始 ISO 字符串
- `freely ai` / watchdog 某些 human-readable cooldown 时间固定显示为 UTC
- 仓库中另一些时间面则天然跟随宿主系统

结果是同一个系统里会同时出现：

- 面向人阅读的 UTC 时间
- 面向人阅读的本地时间
- 面向机器的 epoch / ISO

这会增加理解成本。

### 3. “备份时间”本身在行业里也不是单层概念

行业实践通常把它拆成：

- canonical event/store time
- schedule time / business-local wall clock
- display time

如果不先把边界说清楚，就很容易误把“显示层用本地时间”推广成“备份文件名和审计真相也应该本地化”。

## 官方参考与行业做法

### 1. canonical store truth 倾向 UTC / 可比较时间基准

官方资料普遍把审计、日志、事件时间作为统一真相面处理。

- Oracle Log Analytics best practices 明确建议把系统时间设为 UTC，或把日志时间改为 ISO 8601，目标是保证摄取与比较稳定。
- JavaScript/前端生态中，`Date.prototype.toISOString()` 也明确输出 UTC 时间表达，适合作为序列化真相面。

参考：

- Oracle Log Analytics FAQ / best practices: https://docs.public.content.oci.oraclecloud.com/en-us/iaas/log-analytics/doc/best-practices.html
- MDN `Date.prototype.toISOString()`: https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Date/toISOString

### 2. schedule / user-facing planning 可以按本地时区表达

AWS Backup 专门新增了 local time zone selections，说明“计划在业务本地时区表达”是独立需求，而不是把所有备份真相都变成 local-only。

参考：

- AWS Backup local time zone selections: https://aws.amazon.com/about-aws/whats-new/2023/08/aws-backup-local-time-zone-selections/

### 3. display layer 应按宿主或用户选择时区格式化，并带时区信息

MDN `Intl.DateTimeFormat` 的默认行为是使用运行时当前 locale / time zone；这意味着前端与 CLI 的显示层完全可以保留底层 UTC/ISO 真相，同时按宿主系统时区渲染。

参考：

- MDN `Intl.DateTimeFormat`: https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Intl/DateTimeFormat/DateTimeFormat

## 收敛判断

### 1. 备份命名时间应继续使用 UTC / 稳定排序时间

适用面：

- 备份文件名
- `.bak.<timestamp>`
- history manifest 文件名
- 版本号 / build 命名

原因：

- 这些字段首先服务于排序、恢复、比对和治理，不是人类的主阅读面
- UTC / 单一时基最稳，且本仓库宪法已经把备份命名 UTC 固化为硬性约束

### 2. 机器存储时间应继续保留 epoch / ISO / RFC3339

适用面：

- `occurredAt`
- `reset_at`
- `timestamp`
- 各类 JSON / TSV / cache / event payload 中的真相字段

原因：

- 应让“时间真相”与“显示格式”解耦
- 后续无论是前端、CLI 还是 TUI，都可以在展示层各自格式化

### 3. 面向人的显示时间应默认按当前系统时区渲染

适用面：

- probe UI 最近事件
- CLI human-readable status 字段
- watchdog / cooldown 的 human-readable 辅助列

要求：

- 显示时必须带时区缩写或等价值
- 底层原始值仍保留
- 当输入无法解析时保留原值，不要伪造时间

### 4. 最佳方案不是“全部 UTC”也不是“全部本地时间”

本研究结论：

- naming truth: `UTC`
- storage truth: `epoch | ISO8601/RFC3339`
- display truth: `system local time with timezone label`

这是当前最稳的行业组合，也是最适合 Freely 现有 CLI + runtime + frontend 混合表面的做法。

## 本轮落地范围

当前 worktree 已把上述结论应用到已识别的用户显示面：

- `src/frontend_probe_v0/AppShell.tsx`
- `src/frontend_probe_v0/timeDisplay.ts`
- `docs/system/workspace/scripts/runtime/ai-cli`
- `docs/system/workspace/skills/watchdog-control-plane/scripts/availability-watchdog.sh`

仍未扩展到：

- 全仓所有历史文档中的叙述性日期
- 任何宪法明确要求保留 UTC 的备份命名 / 治理命名规则
- 尚未 materialize 的 future TUI / GUI surfaces

## 下一跳建议

1. 保持备份命名 UTC，不做本地化改动。
2. 对所有新增人类显示时间 surface，统一要求“原始值 + 本地时区渲染 + 时区标签”。
3. 若要把这条边界升级为 repo-wide capability / governance，要进入 owner issue，不能只停留在当前 worktree patch。
