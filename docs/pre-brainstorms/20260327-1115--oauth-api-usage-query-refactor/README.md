# OAuth API Usage Query 重构预研

## 核心判断

1. **OAuth usage API 值得升级为主 inventory 探测面**：可并行扫描全部 `.ai-auth/*/auth.json`，不消耗 token，且不需要把授权文件复制到 `~/.codex/auth.json`
2. **cooldown 文件应恢复并持续维护**：但职责改为 inventory 账本与 reset hint，不再单独决定切号
3. **真实 auth 切换保留到 launch-time**：只有当 watchdog / `switch auto` 已经从 OAuth sweep 选出候选 slot 后，才把对应授权文件复制到 `~/.codex/auth.json`

## 背景：发现 OAuth API

通过研究 CodexBar 项目，发现 OpenAI 提供内部 API：

```text
GET https://chatgpt.com/backend-api/wham/usage
Authorization: Bearer <access_token>
```

返回体不只包含 rate-limit 信息，也可能直接返回：

```json
{"detail":{"code":"deactivated_workspace"}}
```

## 当前痛点

当前全量探测路径的问题：

1. 要串行切 slot
2. 要复制授权文件到 `~/.codex/auth.json`
3. 真实 probe 会消耗 token
4. N 个账号的全量扫描耗时高

## 本轮实测结论

使用本机 `.ai-auth/codex-*/auth.json` 直接并行请求 `wham/usage`：

- 扫描总量：25 个 slots
- 总耗时：约 3.7 秒
- `~/.codex/auth.json` 前后 hash 不变，说明扫描路径不会触碰当前活跃授权位
- 返回分布：
  - `usable`: 8
  - `rate_limited`: 1
  - `deactivated_workspace`: 16

这证明 OAuth sweep 已经足够承担“全量 inventory 真相层”。

## 新架构摘要

```text
.ai-auth inventory
  -> OAuth parallel sweep
  -> availability cache
  -> cooldown ledger overwrite
  -> select best candidate
  -> launch-time auth copy to ~/.codex/auth.json
  -> optional final confirmation probe
```

## 结论

这条 lane 不应再把“串行真实 probe 扫全仓”当作 canonical 主路径。更合理的结构是：

- OAuth sweep：主 inventory 面
- cooldown ledger：由 sweep 全量覆盖维护
- 真实 probe：降级为 launch-time confirmation

## 文件

- `brainstorms.md`：详细架构与分层重构
- `candidates.md`：可执行候选与落地顺序
