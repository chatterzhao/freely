# Brainstorms: raw-20261105T121046Z

## 问题

合并到 develop 之后，安装态不会被重新打包，也没有任何检查能发现「安装态已落后于真源」。

## 证据（2026-11-08 实测，本轮开工前）

- `~/.freely/versions/latest` → `20261108T1050Z-nightly`，其 `.freely_version` 写 `FREELY_PACKAGED_FROM=444985f50`。
- 同一时刻 develop 已是 `c1949aa24`（R15 = #4187 合并提交）—— **安装态落后一个 merge**，issue 描述的症状当场复现。
- `~/.local/bin/freely` 目前指向项目真源 `…/freely/bin/freely`（R5.5 现场规避），不是设计保证：issue 记录它曾是悬空链接且 PATH 优先于项目 `bin/`。
- `bin/freely-package` 只按 allowlist 复制 + 写 `FREELY_VERSION/PACKAGED_AT/PACKAGED_FROM`，**不写关键文件 hash、不切换 `latest`、不重建 `~/.local/bin/freely`**。
- `docs/system/workspace/scripts/worktree/pr-merge-guarded` 的 followthrough 只有 `attempt_develop_push_followthrough_if_needed()`（develop push），grep 不到任何 package/activate 触发点。
- `runtime/freely` 有 `cmd_doctor()`（24585）与 `doctor)` 分派（26841），但不做安装态一致性检查；`FREELY_HOME`（1213 行）可用于隔离测试。

## 证伪（未被现有 open issue 覆盖）

- #4192（R5 已合并）修的是 worktree seed 缺文件，不是安装态版本同步。
- #4205（R5.5 已合并）修的是 allowlist 遗漏，打包能跑通，但没解决「合并后何时打包」与「如何证明一致」。
- #4198（R1 已合并）是门禁性能批量化；#4151 是测试证据链；均与安装态版本无关。
- 本轮 R15（#4187）只改 severity 数据链，未触及打包。

## 关键设计

1. **单一检查真源**：新增 `docs/system/workspace/scripts/quality/install-state-check.py`，输入 `--project` 与 `--home`（默认 `FREELY_HOME` 或 `~/.freely`），输出结构化结论；`freely doctor` 调用它。检查项：
   - `versions/latest` 是否存在/悬空；
   - `.freely_version` 的 `FREELY_PACKAGED_FROM` 是否等于 `git -C <project> rev-parse HEAD`（短 hash 前缀匹配）；
   - 关键真源文件 hash 清单与安装态副本是否一致；
   - PATH 解析到的 `freely` 是否为悬空链接或指向已删除版本。
2. **打包写 hash 清单**：`freely-package` 在 `.freely_version` 追加 `FREELY_HASH_<path>=<sha256>`，供检查复用。
3. **原子切换**：`freely-package --activate` 在打包成功后原子替换 `latest` 并重建链接；失败保留旧版本，绝不留下悬空链接。
4. **受控触发**：`pr-merge-guarded` 的 develop followthrough 在合并成功后调用带 `--activate` 的打包，重复执行幂等（同 HEAD 不重复建版本）。
5. **测试全程隔离**：所有行为用例用临时 `FREELY_HOME` + 临时 git 项目树，**不触碰真实 `~/.freely` 或 `~/.local/bin`**。

## 被否决的替代方案

- 只在 `freely doctor` 打印提示而不落 hash 清单：无法机器证明「关键文件也一致」。
- 每次调用 `freely` 时自动打包：把部署动作塞进每个命令，副作用不可控。
- 用 `git worktree`/软链把安装态直接指向项目树：dev 与安装态耦合，打包产物失去独立可复现性。
- 在 hook 里无条件 `rm -rf ~/.freely/versions/*`：违反个人目录安全边界，且破坏回滚能力。
