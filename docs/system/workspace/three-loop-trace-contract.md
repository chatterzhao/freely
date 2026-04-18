# Three-Loop Trace Contract

Freely 的主链 trace 不是普通 debug 文本，而是三 loop 执行链的 machine-readable handoff 记录。

目标：
- 让人和 AI 都能低成本看出当前在哪个逻辑点
- 看出当前节点从哪里进来
- 看出当前节点出去后应该交给哪里
- 一旦后继没出现，或实际进入点不符合上游声明，能直接定位断链点

## 1. 适用范围

本合同适用于：
- `auto-loop`
- `doc-loop`
- `dev-loop`

不允许用零散自然语言日志替代主链 trace。

普通运行日志可以继续存在，但主链判断一律看 lifecycle trace。

## 2. 节点命名

每个可判定逻辑节点必须有稳定 checkpoint 编号。

当前 loop 前缀约定：
- `A` = `auto-loop`
- `D` = `doc-loop`
- `V` = `dev-loop`

主链显示 ID 规则：
- auto 侧 `L310` 记为 `A-L310`
- doc 侧 `DOC-120` 记为 `D-DOC-120`
- dev 侧 `DEV-220` 记为 `V-DEV-220`

编号要求：
- 编号稳定，不因日志文案变化而漂移
- 新增节点时，必须同时定义它的上游入口和下游交接
- 如果一个节点可能分支到多个下游，要在不同分支出口分别打印不同的 `OUT to=...`

## 3. 一节点两条主链日志

每个节点至少输出两条主链日志：
- `ph=IN`
- `ph=OUT`

含义：
- `IN` 表示逻辑已进入该节点
- `OUT` 表示该节点本轮执行完成，并声明下一跳应交给谁

这两条日志都属于同一个 `me=` 节点。

## 4. 主字段

主链字段固定顺序如下。

`IN`：
- `seq`
- `ph=IN`
- `me=<current checkpoint>`
- `fr=<upstream checkpoint | ENTRY | UNSET>`
- `ok=<1|0>`，仅当当前节点已知上游声明时打印
- `checkpoint=<raw checkpoint>`
- `stage=<stable stage name>`

`OUT`：
- `seq`
- `ph=OUT`
- `me=<current checkpoint>`
- `to=<actual next checkpoint | TERM | UNSET>`
- `ok=<1|0>`
- `checkpoint=<raw checkpoint>`
- `stage=<stable stage name>`

辅助字段只允许放在主字段之后，例如：
- `intake_id`
- `status`
- `classification`
- `session_id`
- `prompt_file`
- `cycle_log`

## 5. 特殊值

- `ENTRY`: 合法外部入口，没有上游 checkpoint
- `TERM`: 当前链路在这里结束
- `UNSET`: 该节点没有正确声明上游或下游，属于 trace 设计缺口，必须尽快补齐

要求：
- 真正入口只能写 `ENTRY`
- 真正结束只能写 `TERM`
- `UNSET` 不是正常设计，只是显式暴露缺口，避免静默失真

## 6. ok 的判定

`IN` 上的 `ok=`：
- `1`: 实际进入点符合上游节点声明的下一跳
- `0`: 实际进入点不符合上游声明，属于断链或错链

`OUT` 上的 `ok=`：
- `1`: 当前节点已明确写出实际下一跳 `to=`
- `0`: 当前节点没有声明下一跳，属于可观测性缺口

## 7. 断链判定

以下任一情况都可判定为链路异常：
- 某节点只有 `IN` 没有 `OUT`
- 某节点 `OUT to=...` 后，应到的下游长期未出现
- 下游节点 `IN ok=0`
- 节点 `OUT ok=0`，说明没有定义下一跳
- 非入口节点的 `IN fr=UNSET`

因此调试时先看：
1. 最后一个 `OUT`
2. 它声明的 `to=`
3. 目标节点是否出现对应 `IN`
4. 目标节点 `IN ok` 是否为 `1`

## 8. 设计原则

- 主链字段要短，固定顺序，方便 grep 和 AI 解析
- `stage=` 保留简短稳定语义，不能写成长段自然语言
- 业务细节放辅助字段，不污染主链
- 任何新增 loop 节点，都必须同时补：
  - 节点编号
  - `IN`
  - `OUT`
  - 上游 `fr`
  - 下游 `to`
- `to` 的打印权归“真正决定下一跳的那一层”所有；不要让纯 helper 硬凑假的下一跳
- 不需要把所有底层函数都变成 lifecycle 节点。只给真正的逻辑节点 / 路由节点编号，避免日志和参数污染

## 9. 示例

```text
2026-04-17T12:00:00Z seq=101 ph=IN me=A-L300 fr=ENTRY checkpoint=L300 stage=intake_recorded intake_id=i-123
2026-04-17T12:00:00Z seq=102 ph=OUT me=A-L300 to=A-L310 ok=1 checkpoint=L300 stage=intake_recorded intake_id=i-123
2026-04-17T12:00:01Z seq=103 ph=IN me=A-L310 fr=A-L300 ok=1 checkpoint=L310 stage=intake_claimed intake_id=i-123
2026-04-17T12:00:01Z seq=104 ph=OUT me=A-L310 to=A-L330 ok=1 checkpoint=L310 stage=intake_claimed intake_id=i-123
```

如果真实逻辑错进了别的节点，应该出现：

```text
... ph=IN me=A-L320 fr=A-L300 ok=0 ...
```

这表示：
- 实际从 `A-L300` 进入了 `A-L320`
- 但 `A-L300` 声明的下一跳并不接受这个进入

## 10. 维护要求

未来修改三 loop 执行逻辑时：
- 先改逻辑，再同步改 trace 编号和 handoff
- 不允许新增匿名跳转
- 不允许只打进入不打出去
- 不允许只写自然语言“下一步做什么”，而不写 `to=<checkpoint>`
