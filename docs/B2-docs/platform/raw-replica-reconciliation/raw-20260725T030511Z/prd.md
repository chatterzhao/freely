# PRD: 配置平台 raw 副本一致性

## Goal

把平台副本读取与一致性判断收束为单向数据流：

`configured platforms → transport records → canonical projection → reconciliation receipt → lifecycle gate`

gate 为只读。任何 create、条件 edit 或评论补齐属于独立 resolution 命令，完成后必须重新读取生成新的 receipt。

## Modules

- `platform-adapter.py`：平台注册、配置读取和平台 transport；统一返回带平台命名空间的 raw 副本记录。
- `raw_reconciliation.py`：纯函数；规范化 raw-key、计算 content fingerprint、比较副本、生成 receipt。
- lifecycle wrappers：仅通过 receipt 判断是否继续；不得各自重建平台比较逻辑。
- scan：消费同一 discovery 结果；平台失败标为 `unknown/degraded`，不得空集合化。

## Invariants

- configured platform 缺副本、重复匹配、不可达或分页不完整一律阻塞写操作。
- platform ID、URL、观测时间不是 canonical 内容；标题、正文、state、labels 与语义评论集合是。
- receipt 仅描述观察与判断，不写磁盘、不调写平台接口。
- local B1 参与 `post-materialize` 与后续 lifecycle 的比较；`materialize` 只比较平台副本。

## Dev-loop handoff

先以纯函数测试证明大小写 key、empty result、多平台一致、缺副本、内容差异和不可达平台的 receipt；再将 adapter 与 lifecycle 入口接到该边界。
