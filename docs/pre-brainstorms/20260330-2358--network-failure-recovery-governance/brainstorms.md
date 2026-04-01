# 预研头脑风暴：network-failure-recovery-governance

## 背景

这轮 dogfood 里，围绕 `auth_failure`、`rate_limit`、代理可用性和网络抖动，已经出现了几种容易混淆的现象：

- `402 Payment Required` / `deactivated_workspace` 已被当前 runtime 归到 `auth_failure`
- Codex usage limit 已被归到 `primary_rate_limit_exhausted` / `secondary_rate_limit_exhausted`
- `ai switch codex` 的 OAuth inventory 刷新打不通时，`ai-cli` 会返回 `oauth_unreachable`
- 但主 supervisor 对“运行中的 `codex exec` 因网络/代理失败而退出”没有单独建模，目前更像退化成普通 `ai_exit_rc_*`

这说明 Freely 现在并不是“完全没有网络治理”，而是网络问题只在局部路径上被识别：

- launch / switch 前的 OAuth 探测有专门语义
- 运行期的通用网络失败还没有独立的错误分类与恢复策略

## 已确认事实

### 1. Freely 当前已经有 `oauth_unreachable` 语义，但只存在于账号切换入口

`docs/system/workspace/scripts/runtime/ai-cli` 当前在 Codex inventory 刷新失败时会：

- 返回 `status=oauth_unreachable`
- `launch_blocked=true`
- 显式提示检查项目级或全局级代理配置
- 不再 silent fallback 到 `codex exec` 探测

现有测试 `docs/system/workspace/scripts/tests/test-freely-ai-account-switch-oauth-unreachable` 已经锁住这条行为。

因此，“OAuth inventory 打不通”这类故障的当前 contract 是清晰的：

- 这是 launch-blocking 的前置网络故障
- 不是账号额度问题
- 不是普通 auth failure

### 2. Freely 当前没有把运行期通用网络故障从普通 AI 退出里分离出来

主 supervisor 的异常分流目前重点识别：

- structured usage / `usage limit`
- `401/402`、`deactivated_workspace`、`subscription expired` 等 auth failure

但没有看到对以下运行期网络错误的单独分类：

- DNS 失败
- 代理连接拒绝 / 代理不可达
- TCP connect timeout
- TLS handshake / upstream reset
- `502/503/504` 这类短暂上游不可用

这意味着：

- 如果 `codex exec` 在运行中因为代理或网络问题退出
- supervisor 很可能只会把它视为 `ai_exit_rc_*`
- 然后进入普通重启与 restart-storm 保护逻辑

也就是说，Freely 当前对“网络故障”缺少一条和 `auth_failure` / `rate_limit` 对等的 canonical bucket。

### 3. 当前代码已经隐含两种不同的网络问题，但还没有显式词典

当前至少存在两类性质完全不同的“网络问题”：

1. preflight / inventory 网络问题
- 发生在 `ai switch`、OAuth refresh、slot probe 前
- 特征是系统连“哪个 slot 可用”都判断不了
- 当前已有 `oauth_unreachable`

2. in-flight execution 网络问题
- 发生在 manager / worker 已经启动之后
- 特征是工具进程中途失败，通常伴随 timeout、连接错误、上游不可用
- 当前缺少显式分类

把这两类继续混成同一个 `network unavailable`，会让恢复策略失真。

## 行业里的常见应对

行业通行做法并不是“看到网络错就一直重试”，而是先判断错误是否短暂、是否可重试、是否幂等、是否已经进入持续性故障。

从 AWS、Google Cloud、Azure、Google SRE 这几条官方资料可以归纳出同一组原则：

1. 先区分 transient 和 non-transient
- 可短时恢复的连接/拥塞/上游暂不可用，才适合自动重试
- 明确的配置错误、永久认证错误、不满足前置条件，不应重试

2. 自动重试必须有边界
- 使用有限次数
- 使用指数退避
- 加 jitter
- 优先尊重服务端给出的 `retry-after` / reset 时间

3. 不要让 retry 放大故障
- 避免多层同时重试
- 需要 retry budget / circuit breaker
- 连续失败超阈值后应快速失败或进入 open state，而不是无限 relaunch

4. 只对幂等操作自动重试
- 读操作、探测操作、resume 探测、status 刷新通常更适合自动 retry
- 可能引起重复副作用的写动作必须先保证幂等或去重

5. 观测面必须能区分“偶发抖动”和“持续故障”
- 单次 transient failure 不该直接升级成事故
- 但持续升高的 retry 次数与失败窗口应成为明确信号

## 对 Freely 更合理的分层

Freely 不应只有一个模糊的 `network_failure`。更合理的是至少分成四类：

### A. `proxy_config_invalid`

定义：

- 项目或全局配置声明 `FREELY_NETWORK_PROXY_MODE=explicit`
- 但实际没有可用代理值，或代理配置明显非法

应对：

- fail fast
- 不启动 manager / worker
- 不做 slot switch
- 直接返回 operator-actionable 错误

理由：

- 这是本地配置错误，不是 transient fault
- 重试不会让配置自动变正确

### B. `oauth_unreachable`

定义：

- 账号 inventory / OAuth refresh 阶段网络不可达
- 当前连 slot 真相都拿不到

应对：

- launch blocked
- 不 fallback 到 `codex exec` 探测
- 不做 account switch
- 给出检查代理与网络的明确提示

理由：

- 如果 inventory 真相缺失，后续账号选择全都不可信

### C. `execution_network_transient`

定义：

- manager / worker 已启动
- 运行中的 `codex exec` 因短时网络抖动、代理超时、`502/503/504`、连接 reset 等退出
- 仍有较高概率短时恢复

应对：

- 不切账号
- 不归到 auth failure
- 同 slot、同 tool 做有限次数 retry
- 使用指数退避 + jitter
- 若有 resume evidence，优先 `resume`
- 若达到本地预算仍失败，则写出明确的网络类 exit reason，交给更高层 watchdog 判断

理由：

- 这类故障的主因是连通性，不是账号或工作区失效
- 直接切账号容易把网络问题误判成 slot 问题

### D. `execution_network_persistent`

定义：

- 在一个滑动窗口内持续发生网络失败
- 或健康探测明确表明代理 / 上游长期不可达

应对：

- 打开 circuit breaker / cooldown
- 暂停 blind relaunch
- 把事件升级为控制面可见的网络不可用态
- 等待明确的 recheck 时间或外部恢复信号

理由：

- 长时 outage 下继续自旋只会制造 churn 和误告警
- 这类故障更接近“依赖面不可用”，应进入受控等待

## Freely 应采用的恢复策略

### 1. 入口前置阶段：先把配置错误和连通性错误分开

建议 contract：

- `proxy_config_invalid`: operator-fix, no retry
- `oauth_unreachable`: bounded recheck, no launch

这里不应走 account-switch，更不应伪装成 `auth_failure`。

### 2. 运行中阶段：把网络故障从通用 `ai_exit_rc_*` 里提升出来

建议 contract：

- 首次或少量短时失败：
  - 记为 `execution_network_transient`
  - 在本地 workcell 内做有限 retry
- 窗口内持续失败：
  - 升级为 `execution_network_persistent`
  - 进入 cooldown / circuit open
  - 停止 blind relaunch

### 3. 切账号必须是最后手段，不应作为网络故障默认动作

只有在以下条件同时满足时，才适合把问题往 slot / account 不可用方向推：

- inventory 真相是可信的
- 当前失败已明确不是代理或网络路径问题
- 出现的是 quota / auth / workspace deactivation 这类 slot-specific 证据

否则，把网络故障映射成账号故障，会让 Freely 进入错误的恢复支路。

### 4. 需要显式的 retry budget，而不是只靠 restart-storm 被动兜底

restart-storm 保护是最后兜底，不是网络恢复策略本身。

更合理的结构应是：

- 每类网络故障有单独预算
- 在预算内按 backoff 重试
- 预算耗尽后 open circuit
- restart-storm 只负责拦截实现失控或未知回路

否则，Freely 只能在“普通 relaunch”和“重启风暴兜底”之间摆动，恢复语义太粗。

## 当前判断

Freely 在网络故障上的现状可以概括为：

- preflight / OAuth refresh 阶段：
  - 已有部分正确建模
  - 当前行为基本合理
- execution 阶段：
  - 还没有 canonical network failure taxonomy
  - 目前的 supervisor 行为不够符合行业最佳实践

因此，这条线的第一跳不应该是直接加一个宽泛正则去匹配所有网络错误，而应该先冻结：

1. Freely 的网络故障词典
2. 每一类的 retry / cooldown / circuit / escalation contract
3. 哪些动作允许自动 retry，哪些必须 fail fast

## 初步方向

更稳妥的后续 issue，应该围绕以下边界展开：

1. 建立 `proxy_config_invalid` / `oauth_unreachable` / `execution_network_transient` / `execution_network_persistent` 的 canonical state
2. 在 supervisor 中把运行期网络故障从 `ai_exit_rc_*` 分流出来
3. 引入 bounded retry + exponential backoff + jitter + retry budget
4. 用 circuit-open / cooldown 取代长时 outage 下的 blind relaunch
5. 补一组 focused regressions，覆盖：
   - 代理配置错误
   - OAuth inventory 不可达
   - 短时运行期网络失败
   - 持续运行期网络失败

## 外部参考

以下官方资料支持上述方向：

- AWS Prescriptive Guidance: retry with backoff pattern
- AWS Well-Architected: set client timeouts / control and limit retry calls
- Google Cloud: exponential backoff with jitter, and retry only when response + idempotency criteria are satisfied
- Google SRE: randomized exponential backoff, retry budgets, avoid multi-layer retry amplification
- Azure Retry pattern / transient fault guidance / retry storm antipattern
