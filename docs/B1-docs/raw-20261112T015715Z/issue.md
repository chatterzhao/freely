---
schema_version: '1'
local_id: raw-20261112T015715Z
kind: raw
phase_state: absorbed
absorbed_into: I-20261112T015715Z-A
platform_ids:
  github:
    issue_id: '4307'
    url: https://github.com/chatterzhao/freely/issues/4307
    synced_at: ''
  gitee:
    issue_id: IKUR3Z
    url: https://gitee.com/zhaoquan/freely/issues/IKUR3Z
    synced_at: ''
primary_platform: github
canonical_issue_path: docs/B2-docs/gate/ci-machine-independence/raw-20261112T015715Z/issues/I-20261112T015715Z-A.md
last_synced_comment_at:
  github: '2026-11-12T02:18:17Z'
  gitee: '2026-11-12T02:18:17Z'
hash: ''
created_at: '2026-11-12T01:57:15Z'
updated_at: '2026-11-12T03:04:03Z'
intake_id: ''
author: platform
channel: github
session_refs: []
platform_state: closed
promoted_children:
- I-20261112T015715Z-A
source_candidate: ''
completed_at: '2026-11-12T02:18:16Z'
closeout_note: ''
severity: P2
---

# fix: test-contract-single-source 的 cline 断言依赖本机安装，CI 恒红

workflow_kind: fix

## fix: test-contract-single-source 的 cline 断言依赖本机安装，CI 恒红

| Field | Value |
|-------|-------|
| local_id | `raw-20261112T015715Z` |
| kind | `raw` |
| phase_state | `proposed` |
| canonical | `none` |
| created | 2026-11-12T01:57:15Z |
| updated | 2026-11-12T01:57:15Z |

---

> **Freely 治理**：这是 raw issue `raw-20261112T015715Z`。实现前请用 `wt-create --raw-key 20261112T015715Z` 创建专属工位，确保代码修改在包含此 raw-key 的分支上进行。

## 现象

在 develop 基线 27e91e50c 与 R33 分支 92052ebf8 上分别直接运行 docs/system/workspace/scripts/tests/test-contract-single-source.py，均得到 SUMMARY: 12 ok, 1 failed，唯一失败项为 [FAIL] registry present: registry tools are read (cline detected)。因此 bin/test-all --ci 在本机恒为 20 ok, 1 failed，freely test-gate run 记录 TEST_STATUS=failed / TEST_EXIT_CODE=1，pretests-retirement-gate 与 wt-close 会据此拦截，任何 issue 都无法收口。

## 根因

bin/deploy-skills 第 77-98 行按 registry 逐项解析 test_command 的第一个词，再用 command -v 判定工具是否 installed；cline 段的 test_command 是 cline 'say hi' --auto-approve true，本机 PATH 中不存在 cline 二进制，因此 --dry-run 只输出 claude 一项。而测试第 143-149 行把输出里出现字符串 cline 当作 registry 被成功读取的证据。测试把「本机安装了 cline」当成了未声明的隐含前提，与产品侧已演进为「只部署已安装工具」的语义发生契约漂移。这不是断言写错，而是断言绑定了机器状态。

## 复现与证伪

1. command -v cline 在本机（含 login shell /opt/homebrew/bin 等）均不存在；~/.freely/tool-registry.toml 不存在；query --list 正常返回 claude/cline/codex/opencode。
2. develop 基线与 R33 分支同样 12 ok, 1 failed → 非 R33（#4179）引入，属预存缺陷。
3. 在临时目录放一个可执行的 cline stub 并前置到 PATH 后，develop 基线与 R33 分支都变为 13 ok, 0 failed，其余 12 条静态/行为断言及 registry missing fail-closed、explicit --tools 全部保持通过 → 失败仅来自缺失的环境前提，补齐后测试真正执行到它想验证的 registry 读取路径，未掩盖任何断言。

## 影响

跨 issue 阻塞级：所有后续轮次在无 cline 的机器上重刷 test-gate 都会红，只能靠人工临时 PATH shim 绕过（R33 收口即如此处理，已在 goal 恢复点如实留痕）。CI 结果不再具备机器无关性，与 test-all --ci 作为验收子集的定位冲突。

## 建议方向（供 B1 预研，不在本轮实现）

1. 首选：测试自行在 tempfile 目录中创建 stub 并注入 PATH，使断言验证 registry 读取逻辑而非本机工具安装状态；同时保留 registry missing / explicit --tools 两条行为断言。
2. 备选：把断言改为验证 deploy-skills 对 registry 的解析行为（例如显式 --tools 或注入式 fake query），彻底去掉对 command -v 结果的依赖。
3. 验收：在无 cline、无 codex、无 opencode 的干净 PATH 下，test-all --ci 仍为 21 ok, 0 failed；且把 registry 文件改名后对应断言仍判红（不退化 fail-closed）。

## 评审结论

真实、可复现、跨 issue 阻塞，且已在 develop 基线证伪为本轮引入，应作为独立 fix raw 登记；R33 已合并收口，本条不回灌 R33 代码。

### comment-20261112T021817Z
- source: system
- event: promote_finalized
- children: ["I-20261112T015715Z-A"]

拆解为以下任务:
1. [I-20261112T015715Z-A](will-be-updated)
