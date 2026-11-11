# Cross-Process Data Contract（单页）

机器可读真源：`contract.yaml`（JSON 兼容 YAML 1.2 子集，`json.loads` 可读）。
守护：`bin/check-cross-process-contract`（0 通过 / 1 契约违规 / 2 真源缺失）。

跑边界判定：`docs/system/workspace/scripts/quality/cross_process_boundary.py`。

## 为什么需要它

Bash 调 Python 时，三种失败以前长得一模一样：

| 现象 | 以前的后果 |
|---|---|
| 字段缺失 | `values` 对不存在的 key 返回空字符串，调用方分不清「没有」和「空」 |
| 类型错误 | 值被 `str()` 强转，`12345` 变成 `"12345"` 一路往下传 |
| 超时 | 与普通失败共用一个退出码，调用方无法重试或降级 |

## 错误模型

统一信封（只在失败时出现，成功时透传子进程 stdout）：

```json
{"ok": false, "error": {"kind": "missing_field", "message": "...", "source": "..."}}
```

| 退出码 | 含义 |
|---|---|
| 0 | ok |
| 1 | 生产方内部异常 |
| 2 | 用法错误 / 契约真源缺失（不适用） |
| 3 | 契约违规：`missing_field` / `type_error` / `invalid_json` |
| 4 | 超时：`timeout` |

四个 `kind`：`missing_field`、`type_error`、`invalid_json`、`timeout`。

**超时必须可区分**：`timeout` 固定退出码 4，不许退化成 1 或 3 —— 调用方要能
分辨「回答错了」和「太慢了」。

## 状态文件协议（`state_file.py`）

- 写入格式只有一种：`KEY<TAB>JSON字符串`，不可执行。
- 读取兼容 `KEY=VALUE` 旧行，只剥掉一对引号，**不做任何展开**。
- 值永远是字符串，非字符串直接拒绝，不强转。
- 缺失 key：`read_state` 不返回该 key，`values` 返回空字符串 —— 所以**需要该
  key 的调用方必须在边界声明的 `required_keys` 里登记**，由边界 runner 判红。

## 已登记的边界

见 `contract.yaml` 的 `boundaries`：`state-file-read`、`issue-json-read`、
`platform-adapter-json`、`red-evidence-read`。每条声明生产方文件、消费方、
必须存在的 key 以及「为什么不能静默兜底」；lint 会校验生产方文件确实存在。

## 已知缺口（不在本阶段）

1. `scripts/tests/*` 夹具里 22 处 `source *.env` 仍走 shell sourcing —— 是测试
   夹具不是生产生产方，未迁移。
2. 33 处 `|| echo` 多数是 JSON 解析回退，不全是吞错，需逐点复核后再归零。
3. 边界声明的消费方尚未逐点机检：lint 只校验生产方文件与声明本身。
