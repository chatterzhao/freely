---
schema_version: '1'
local_id: raw-20261128T065937Z
kind: raw
phase_state: proposed
absorbed_into: ''
platform_ids:
  github:
    issue_id: '4749'
    url: https://github.com/chatterzhao/freely/issues/4749
    synced_at: ''
  gitee:
    issue_id: IKYNFC
    url: https://gitee.com/zhaoquan/freely/issues/IKYNFC
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-11-28T06:59:37Z'
updated_at: '2026-11-28T06:59:45Z'
intake_id: ''
author: platform
channel: github
session_refs: []
platform_state: open
promoted_children: []
source_candidate: ''
completed_at: ''
closeout_note: ''
severity: P0
---

# fix: 新增命令名契约检查导致打包失败（非运行时工具引用了不随包发布的 commands.md）

workflow_kind: fix

## fix: 新增命令名契约检查导致打包失败（非运行时工具引用了不随包发布的 commands.md）

| Field | Value |
|-------|-------|
| local_id | `raw-20261128T065937Z` |
| kind | `raw` |
| phase_state | `proposed` |
| canonical | `none` |
| created | 2026-11-28T06:59:37Z |
| updated | 2026-11-28T06:59:37Z |

---

> **Freely 治理**：这是 raw issue `raw-20261128T065937Z`。实现前请用 `wt-create --raw-key 20261128T065937Z` 创建专属工位，确保代码修改在包含此 raw-key 的分支上进行。

## 现象\nR59（raw-20261108T134701Z）合并后，pr-merge followthrough 的 install-state 刷新失败：\n[runtime-file-parity] runtime-referenced file missing from package allowlist: docs/system/workspace/commands.md\n[runtime-file-parity] 1 undeclared runtime file(s) - packaging aborted\n\n## 精确根因\n1. R59 在 bin/freely 新注释里写了字面路径 docs/system/workspace/commands.md；bin/ 属于 package-runtime-file-parity.py 的 RUNTIME_DIRS。\n2. R59 新增的 command_name_contract.py 放在 scripts/quality/，该目录也被同一检查器视为 RUNTIME_DIRS；它同样字面引用 commands.md。\n3. 但 commands.md 经 raw-20261106T100938Z 评审明确「不随包发布」，package-allowlist.txt 注释有据。于是只读测试型工具与运行时注释一起触发 fail-closed，打包被阻断。\n\n## 设计判断\n不是 allowlist 漏项：把 commands.md 加入包会推翻 raw-20261106T100938Z 的设计判决。也不是 parity 检查器该放宽：fail-closed 是对的。问题是 R59 把「仅测试期使用的契约检查器」放进了运行时质量目录，且在入口注释里写了不随包发布的文档路径。\n\n## 修复方向\n1. bin/freely 注释只写真实命令，不写 commands.md 字面路径。\n2. command_name_contract.py 移到 scripts/tests/（测试工具，非运行时质量能力），同步 AT 与函数级单测的引用路径。\n3. AT：在 develop 基线复现 package-runtime-file-parity rc=1；修复后 rc=0；原命令名契约 AT 与单测保持全绿，且 checker 仍能抓出合成反例。\n4. 回归：freely-package --version auto --activate 成功。\n\n## 非目标\n不改 package-runtime-file-parity 判据、不扩 package-allowlist、不改 commands.md 是否随包的既有判决。\n\n## 证据\n- merge 8c55a9e09 的 followthrough 输出（packaging aborted）。\n- package-allowlist.txt:49-51「3 个纯文档/测试资料（commands.md / ...）经评审不随包发布」。\n- package-runtime-file-parity.py:36-41 RUNTIME_DIRS 包含 bin 与 scripts/quality。
