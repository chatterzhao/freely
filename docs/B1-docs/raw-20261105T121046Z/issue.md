---
schema_version: '1'
local_id: raw-20261105T121046Z
kind: raw
phase_state: absorbed
absorbed_into: I-20261105T121046Z-A
platform_ids:
  github:
    issue_id: '4194'
    url: https://github.com/chatterzhao/freely/issues/4194
    synced_at: ''
  gitee:
    issue_id: IKT9AV
    url: https://gitee.com/zhaoquan/freely/issues/IKT9AV
    synced_at: ''
primary_platform: github
canonical_issue_path: docs/B2-docs/gate/platform/raw-20261105T121046Z/issues/I-20261105T121046Z-A.md
last_synced_comment_at: {}
hash: ''
created_at: '2026-11-05T12:10:46Z'
updated_at: '2026-11-08T13:43:28Z'
intake_id: ''
author: platform
channel: github
session_refs: []
platform_state: closed
promoted_children:
- I-20261105T121046Z-A
source_candidate: ''
completed_at: '2026-11-08T13:36:59Z'
closeout_note: ''
---

# fix: 合并 develop 后安装态不重新打包，PATH 可能命中旧版 freely 命令

workflow_kind: fix

## 根因

开发态与安装态之间没有任何版本同步机制。项目真源在 git 工作树（`bin/` + `docs/system/workspace/scripts/`），通过 `freely-package` 复制到 `~/.freely/versions/<ver>/` 形成安装态；但打包是一次性手工动作，合并到 develop 之后不会触发，也没有任何检查能发现「安装态已落后于真源」。结果是人/agent 从安装位置或 PATH 启动 `freely` 时，可能执行的是几个月前的旧命令，行为与当前仓库不一致且无提示。

## 证据（本机 2026-11-05 实测）

- `~/.local/bin/freely` 是悬空符号链接，指向 `/Users/zhaoyu/.freely/versions/20260512-nightly/bin/freely`；该版本目录下只有 `projects.tsv`，连 `bin/` 都不存在。
- `~/.freely/versions/latest` -> `20260519T1530Z-nightly`（2026-05-19），比当前 develop 落后近半年。
- 安装态 `docs/system/workspace/scripts/runtime/freely` 为 21,732 行，项目真源为 26,823 行；安装态 `wt-create` 不含本轮已合并的 `resume_mode` / `_new_flags_present` 修复（`grep -c` 为 0）。
- PATH 中 `/Users/zhaoyu/.local/bin` 位于项目 `bin/` 之前（索引 22/23 vs 25）。`~/.zshrc` 的 `@freely-dev-path` 行试图把项目 `bin/` 前置，但 `bin/freely` 注释声明的 `freely install` 会移除该行，而全仓检索不到任何 `install` 命令实现或安装包脚本。当前之所以没命中旧命令，纯粹因为那个链接是悬空的——这是偶然，不是设计保证。
- `freely-package` 只按 allowlist 复制并写 `.freely_version`，不会更新 `latest`，不会重建 `~/.local/bin/freely`；`pr-merge-guarded` 与 `docs/system/workspace/hooks/`、`.githooks/` 中也没有任何打包/部署触发点。
- 开发工位的 `bin/` 来自 git checkout，是最新 develop，这一点正确；风险完全集中在安装态与 PATH 解析。

## 影响

- 从 `~/.freely/versions/latest`、`~/.local/bin/freely`（一旦链接被重建）启动的 `freely` 会静默执行旧版 runtime / 旧版门禁，修复过的缺陷在新会话中「复活」。
- 无法用机器证明「当前生效的 freely == 当前 develop 真源」，自举开发时命令行为不可判定。
- `bin/freely` 注释与 `~/.zshrc` 标记承诺了一套 install/dev-path 切换机制，实现却不存在，属于文档与实现脱节。

## 修复方案

1. 增加版本一致性检查（可由 `freely doctor` 或一个独立命令承载）：解析 `command -v freely` 的实际真身路径，读取安装态 `.freely_version` 的 `FREELY_PACKAGED_FROM`，与当前 develop HEAD 及关键真源 hash 比对；不一致或发现悬空链接时明确报错并给出修复指令，不得静默放过。
2. 在受控时机自动重新打包并切换安装态：合并到 develop 后由 `pr-merge-guarded` 的 followthrough（或受控的独立命令）调用 `freely-package`，成功后原子切换 `latest` 并重建 `~/.local/bin/freely`；切换失败保留旧版本并报错，不得留下悬空链接。
3. 消除实现缺口：要么实现注释承诺的 `freely install`（含 `@freely-dev-path` 标记增删），要么删掉注释与标记，文档只描述真实存在的机制。
4. `freely-package` 写出的 `.freely_version` 增加真源关键文件 hash 清单，供第 1 项校验复用。

## 验收标准

- RED：把 `latest` 指向落后版本后运行一致性检查，断言退出非零且输出指出落后；当前无任何检查。
- RED：`~/.local/bin/freely` 为悬空链接时运行一致性检查，断言被报告；当前静默。
- GREEN：从当前 develop 打包并切换后，一致性检查退出 0，且 `command -v freely` 解析到最新安装态或项目真源，二者代码一致。
- GREEN：`latest` 与 `~/.local/bin/freely` 不出现悬空或指向已删除版本；切换失败时旧版本仍可用。
- GREEN：合并到 develop 后触发的打包步骤有幂等性，重复执行不产生副作用。

## 边界

不改 `wt-create` 的工位 seed 逻辑（工位的 `bin/` 来自 checkout，本身正确）；不改 protected branch 规则；不引入绕过门禁的部署通道。
