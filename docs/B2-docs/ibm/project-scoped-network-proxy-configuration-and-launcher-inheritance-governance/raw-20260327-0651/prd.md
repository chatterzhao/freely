# PRD: project-scoped-network-proxy-configuration-and-launcher-inheritance-governance

## Goal

把 Freely runtime 里的网络代理从“脚本里写死默认值”升级成“项目级配置真源 + 单一 resolver”。

## Product shape

1. `.freely/config.env` 持有 proxy 相关的 project-scoped truth。
2. `freely init` 负责写入 managed defaults。
3. resolver 统一把 project config 映射成运行时 env。
4. codex exec launcher 与 watchdog 的 curl/OAuth 路径都消费同一个 resolver。

## Config contract

建议的项目级字段：

- `FREELY_NETWORK_PROXY_MODE`，取值 `inherit|explicit|disabled`
- `FREELY_NETWORK_PROXY_URL`
- `FREELY_ALL_PROXY`
- `FREELY_HTTP_PROXY`
- `FREELY_HTTPS_PROXY`
- `FREELY_NO_PROXY`

约束：

- `inherit` 表示不改写当前 proxy env
- `explicit` 表示从 `.freely/config.env` 里导出的值覆盖运行时
- `disabled` 表示显式清空 proxy env
- 不允许把 `127.0.0.1:7890` 之类的默认值写进代码作为 fallback

## Runtime contract

1. codex exec 进入 launcher 前应继承 project proxy env。
2. OAuth/curl path 在发请求前应走同一 resolver。
3. watchdog 与 launcher 之间不再各写一套 proxy 判定逻辑。
4. future frontend 只需要修改 `.freely/config.env`，无需直接碰 runtime shell。

## Evaluation

1. focused regression 是否能锁住 init defaults、resolver mode handling 与 launcher inheritance。
2. runtime 是否仍保持 project-scoped truth，而不是隐式使用用户全局 shell 里的偶然 proxy env。
3. 新 resolver 是否足够小，后续可在更多 launcher/path 上复用。
