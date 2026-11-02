# 图片索引（按原文出现顺序）

| 图 | 文件 | 内容 | 用法 |
|---|---|---|---|
| 图 1 | `assets/fig-01.jpg` | 同一任务在 IM 与 GitHub PR 之间连续推进的对话截图 | 证明“跨信道连续”的产品形态 |
| 图 2 | `assets/fig-02.jpg` | 群聊静默监听、无人 @ 主动定位并提交修复 PR | 证明“主动 + 静默观察”的形态 |
| 图 3 | `assets/fig-03.jpg` | 整体架构：Trigger → 两级过滤 → Router → Worker；执行环境、Session DB、Watchdog | 全文总图，模块编号 [2]-[6] |
| 图 4 | `assets/fig-04.jpg` | 双层架构：Router 统一交互，多 Worker 隔离并发 | Router/Worker 职责图 |
| 图 5 | `assets/fig-05.jpg` | 两级过滤：程序层 Fast Path 拦截/放行，语义层 Slow Path 判断 | 事件准入机制 |
| 图 6 | `assets/fig-06.jpg` | Thread 示例：IM 话题 / GitHub PR 下连续 Trigger | Thread 定义 |
| 图 7 | `assets/fig-07.jpg` | 订阅直通：初始事件走 Router 建订阅，后续事件 Fast Path 直达 Worker | 事件路由核心 |
| 图 8 | `assets/fig-08.jpg` | 链式召回：Trigger/Thread/Worker 互相内联 ID，按需多跳读取 | 上下文组织 |
| 图 9 | `assets/fig-09.jpg` | 讨论未结束，后台已提交可靠修复 PR | 投机执行/提前行动 |
| 图 10 | `assets/fig-10.jpg` | 经典 ReAct Loop vs 异步 ReAct Loop（run 阻塞 vs start/stop 非阻塞） | ReAct 意图对照核心图 |
| 图 11 | `assets/fig-11.jpg` | 计算/状态/执行环境分离：云端 Agent Loop、Session DB、端侧 daemon | 存算/执行环境解耦 |
| 图 12 | `assets/fig-12.png` | 工作请求累计到达 vs 四种方案累计完成曲线 | 消融实验结果 |
| 图 13 | `assets/fig-13.png` | 四种方案 P50/P95 与读缓存 token 表 | 实验数据表 |
| 图 14 | `assets/fig-14.png` | Router batch 大小/单请求耗时/单决定分摊推理时间 | 批处理实验 |
| 图 15 | `assets/fig-15.png` | DeepSeek 产品部招聘广告 | 非技术图，仅归档 |
