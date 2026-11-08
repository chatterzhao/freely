# PRD: 安装态版本可证明且与 develop 同步

- issue_id: I-20261105T121046Z-A
- source_raw: raw-20261105T121046Z
- workflow_kind: fix
- milestone: M-20261105T121046Z-A
- story: gate/platform（复用既有 story）

## 目标

`freely doctor` 能机器证明「当前生效的 freely 就是当前 develop 真源」；合并 develop 后受控重新打包并原子切换安装态；落后、悬空、hash 漂移都必须显式报错，不得静默。

## 改动范围（3 个真源 + 2 个新文件 + 1 个测试）

1. 新增 `quality/install_state.py`（唯一真源）与 `quality/install-state-check.py`（doctor 用 CLI）。
2. `bin/freely-package`：hash 清单、`--version auto`、`--activate`、幂等。
3. `worktree/pr-merge-guarded`：合并 followthrough 触发受控重打包。
4. `runtime/freely`：doctor 输出安装态结论。
5. 新增 `tests/test-install-state.py`（AT-001）。

## 功能需求

- FR-1: `latest` 指向落后版本 → 检查 rc≠0 且输出含 `behind`；悬空 `latest` / 悬空 PATH 链接 → 输出含 `dangling`。
- FR-2: 打包写 `.freely_hashes`（6 个关键真源文件的 sha256），检查器据此发现 hash 漂移。
- FR-3: `--activate` 用临时 symlink + `os.replace` 原子切换 `latest`；激活前校验版本文件与清单，失败保留旧版本。
- FR-4: `--activate` 只修复悬空/缺失的 PATH 链接，不覆盖健康链接。
- FR-5: 同一 HEAD 重复 `--activate` 无副作用；合并 followthrough 调用幂等。
- FR-6: 所有行为用例隔离 `FREELY_HOME`，真实安装目录零写入。

## 不退化边界

默认打包行为不变；门禁、生命周期、平台写语义不动；21 个回归零 DIFF。

## 验收

AT-001 基线快照 RED `2 ok / 21 failed` → GREEN `23 ok / 0 failed`；21 个回归全 MATCH；真机：合并后 followthrough 自动把 `latest` 从 `444985f50` 刷新到新 HEAD，`freely doctor` 输出 `install_state: ok`。
