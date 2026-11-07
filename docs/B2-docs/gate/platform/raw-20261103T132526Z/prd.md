# PRD: 平台写通道失败必报、部分成功可追

- issue_id: I-20261103T132526Z-A
- source_raw: raw-20261103T132526Z
- workflow_kind: fix
- milestone: M-20261103T132526Z-A
- story: gate/platform（复用 wt-create 已物化的 story）

## 目标

平台写通道的每一次失败都要可见、可诊断、可重试；「部分成功」既不伪装成成功，也不伪装成全部失败。

## 改动范围（3 个真源 + 1 个测试）

1. `bin/issue-sync`：gitee 写原语对齐真实 CLI（`--repo <repo> <sub> --flag`）、删掉 `GITEE_TOKEN` 判断、`_gitee_repo_from_url` 覆盖三种 URL 形态、`_gh_close` 返回真实状态、`cmd_create` 先落 id 再写 `platform_state` 并按平台记账（0/3/1）。
2. `docs/system/workspace/scripts/sync/platform-adapter.py`：`detect_reason()` 区分未安装/未认证/超时/无权限，`_unavailable_error()` 取代 `unsupported platform`，`create-issue` 退出码 0/3/1。
3. `docs/system/workspace/scripts/runtime/freely`：`cmd_feedback` 用 JSON 解析按平台汇报，部分成功 exit 3。
4. 新增 `docs/system/workspace/scripts/tests/test-platform-write-channel`（AT-001）。

## 不退化边界

- gitee 读通道、`issue-sync close` 的严格路径（`_raw_effect close-platforms`）、`pr-merge-guarded`、`.githooks/` 全部不动。
- `cmd_close` 的部分成功口径归 #4184，本轮只在注释里标注、不改语义。
- 契约常量收口归 #4154，本轮只对齐调用形态。
- 现有 `test-platform-open-parity` / `test-raw-reconciliation` / `test-platform-adapter-*` 基线对比零新增失败。

## 功能需求

- FR-1: gitee 写调用走真实 CLI 契约，失败原样非零，不再产生「合法空结果」。
- FR-2: token 只在 `gitee-issue.py` 读取；bash 侧不再用未赋值的变量跳过整段通道。
- FR-3: `_gitee_repo_from_url` 对 `git@host:owner/repo.git` / `ssh://` / `https://` 均产出 `owner/repo`。
- FR-4: 平台探测失败必须带原因；缺 `gh` 报 `not installed`。
- FR-5: 一成一败 → 退出 3、只落成功平台 id、`platform_state` 不变、可重跑自愈。
- FR-6: `freely feedback` 按平台汇报并区分退出码。

## 验收

AT-001 基线 15 项失败 → GREEN 22 ok / 0 failed；相关回归基线对比零新增失败；真实仓库只读核验 repo 身份与双平台探测。
