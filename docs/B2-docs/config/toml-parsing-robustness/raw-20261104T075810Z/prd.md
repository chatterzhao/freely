# PRD: config schema + doctor 可观测类型校验
- issue_id: I-20261104T075810Z-A
- source_raw: raw-20261104T075810Z
- milestone: M-20261104T075810Z-A

## 问题
`.freely/config.toml` 无 schema；类型错误不报错，消费端静默失效。实证 `[skip_ibm_gate].allowed_paths` 存成字符串，gate 只认 list，豁免从未生效。

## 目标
1. 机器可读契约覆盖全部 58 个配置键。
2. 类型不符 / 未知键 / 必填缺失三类错误带 `文件:行号` 与期望类型。
3. 安装态（无第三方依赖）也能校验。
4. 不改变 gate 的豁免判定语义与 doctor 的退出码契约。

## 非目标
- 合并 `agents/agent-roles.toml` 与 `.freely/agent-table.toml`（#4172）。
- 让 gate 对坏配置 fail-closed（#4157 族，会自锁每轮 PR）。
- 校验 runtime 的 1,521 处 `${VAR:-...}` 隐式变量（超出 config.toml 范畴）。

## 验收
见 verification/pre-tests.md 的 AT-001。
