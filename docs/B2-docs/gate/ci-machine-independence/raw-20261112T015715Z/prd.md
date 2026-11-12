# PRD: registry 契约测试机器无关化

- issue_id: I-20261112T015715Z-A
- source_candidate: docs/B1-docs/raw-20261112T015715Z/candidates.md#C-20261112T015715Z-A
- milestone: M-20261112T015715Z-A

## Goal

让 `test-contract-single-source.py` 在任何机器上都能验证「`deploy-skills` 确实读取了
tool-registry.toml」，而不依赖这台机器是否安装了 cline。修复后，
不带任何外部 shim 的 `bin/test-all --ci` 必须是全绿，`freely test-gate run`
才能重新成为可信、可移植的收口证据。

## 模块划分（从 B1 Decision 推导）

| 模块 | 文件 | 职责 |
|---|---|---|
| M1 环境前提自建 | `test-contract-single-source.py::registry_checks` | 用 `TemporaryDirectory` 生成可执行 `cline` stub，构造子进程专用 `env` |
| M2 断言保持 | 同上 | present / missing / explicit 三条行为断言语义不变 |
| M3 验收机器化 | `scripts/tests/test-ci-machine-independence.py` | AT-001：静态 + 行为 + 负向控制 + 不退化 |
| M4 CI 接线 | `bin/test-all` | `CORE` 与 `CI_CORE` 各加一行 AT |
| M5 能力注册 | `docs/B2-docs/gate/ci-machine-independence/`、`docs/epics-map.svg` | 新 story 与 epics-map 对齐 |

## 实现方案

### M1：stub 的作用域

```python
stub = tmp / "tool-probe-bin"
stub.mkdir(parents=True, exist_ok=True)
probe = stub / "cline"
probe.write_text("#!/bin/sh\nexit 0\n", encoding="utf-8")
probe.chmod(0o755)
env = dict(os.environ)
env["PATH"] = f"{stub}{os.pathsep}{env.get('PATH', '')}"
```

- `tmp` 是测试已有的 `tempfile` 沙箱，`TemporaryDirectory` 退出即清理。
- 用 `dict(os.environ)` 拷贝而非 `os.environ["PATH"] = ...`，不改全局状态、
  不泄漏到同进程其它用例。
- 三个 `subprocess.run` 都显式 `env=env`，保证 present / missing / explicit
  在**同一**环境前提下执行，避免出现「present 有 stub、missing 没有」的假判据。

### M2：为什么负向控制必要

stub 让 `cline` 必然出现在 `--dry-run` 输出，存在「断言变成永真」的风险。
AT-001 因此必须包含一个负向控制：在沙箱里把 registry 的 `cline.test_command`
首词改成一个绝不存在的二进制名，再跑同一测试，期望 `registry present` 断言**判红**。
这证明输出里的 `cline` 来自 registry 读取，而不是被 stub 或硬编码绕过。

### M3/M4/M5

AT 单文件、无外部依赖；`bin/test-all` 只加两行；epics-map.svg 只加一个 story 条目
（保留原有底色与排版，不整份重绘）。

## Dev-Loop Handoff

1. RED：把最终版 AT-001 注入 `git archive develop` 基线快照，确认红且红因正确。
2. 实现 M1→M5，不改任何产品脚本。
3. GREEN：干净 PATH（不含 cline、不设任何 shim）下 AT-001、`test-all --ci`、
   `test-gate run` 三者全绿。
4. 收尾：`pr-create-guarded` → `pr-review-guarded`（Step 2.5 预期 skip，本轮不触达
   `scripts/runtime/`）→ `pr-merge-guarded` → `wt-close`。
