---
local_id: raw-20260629T122254Z54Z
kind: raw
phase_state: absorbed
absorbed_into: I-20260629T122254Z-A
platform_ids:
  github:
    issue_id: '3622'
    url: https://github.com/chatterzhao/freely/issues/3622
    synced_at: ''
  gitee:
    issue_id: IJXNZU
    url: https://gitee.com/zhaoquan/freely/issues/IJXNZU
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-06-29T12:23:16Z'
updated_at: '2026-06-29T12:23:16Z'
intake_id: ''
author: platform
channel: github
session_refs: []
---

\n\n## 背景

全链路中的 [cmd] 节点目前部分有 freely 入口、部分只有 ./bin/ wrapper、部分完全没有 freely 入口：



## 需要做的事情

### 1. 补全 freely 子命令
所有 [cmd] 节点必须有对应的 freely xxx 入口：
-  — 当前只有 bin/pr-review-guarded，需注册为 freely 子命令

### 2. wrapper 脚本与 freely 入口的一致性
-  等 wrapper 是否继续保留（向后兼容）还是删除
- 如果保留，确保 wrapper 内容与 freely 入口一致

### 3. 全链路引用更新
所有文档、skill、hook、脚本中引用的命令路径：
-  → 
-  → 
- Usage:
  ./bin/pr-merge-guarded <target-branch> <source-branch> [--dry-run]
  ./bin/pr-merge-guarded complete <target-branch> <source-branch>

Behavior:
  - non-interactive policy gate before merge
  - blocks invalid merge direction immediately
  - supports fix/*, feature/*, feat/*, hotfix/*, release/* source branches
  - writes protected-branch merge receipts into merge commit messages
  - supports a controlled conflict completion path
  - --dry-run: run all gates but skip git merge/issue-sync/develop-push
  - gate bypass (--no-verify, etc.) is permanently forbidden → 
- Usage:
  ./bin/wt-create --raw-key <key> --source platform --kind <fix|feature|hotfix> --slug <slug> [--base <branch>]
  ./bin/wt-create <branch> [--base <base-branch>]    (legacy: 补建 test-pre-merge-*、纯文档、init develop、release 分支)

Required:
  --raw-key <key>     Raw issue key (YYYYMMDDTHHMM[SS]Z format, e.g. 20260513T010343Z)
  --source  platform    Raw issue must exist on a configured platform (created via 'freely feedback')
  --kind    <fix|feature|hotfix>    如何选择 → 见下方「--kind 选择指南」
  --slug    <slug>    Short descriptive slug for the worktree

Optional:
  --base <branch>     Base branch (default: develop)
  --skill  <name>     Override workflow skill (default: freely-workflow-guarded-execution)

── --kind 选择指南 ──────────────────────────────────────────

  --kind 决定两件事: ① 分支前缀（fix/ 或 feature/）
                    ② RED 阶段怎么做（fix RED = 复现，feature RED = 设计新测试）

  --kind fix     bug 可以稳定复现。
                 已有测试能捕获 → 直接跑，确认 FAIL。
                 没有测试 → 设计复现测试或手工端到端复现。
                 RED 含义: bug 存在时按测试方法测试一定是 RED，修复正确后，用修复前一样的测试方法，结论一定是 GREEN
                 分支: fix/raw-{raw-key}-{slug}

  --kind feature 新功能、重构、优化、架构改进。
                 RED 阶段按端到端→集成→单元设计新测试，全部 FAIL 才进 dev。
                 RED 含义: 功能未实现时，按测试方法测试一定是 RED，实现正确后，用实现前一样的测试方法，结论一定是 GREEN
                 分支: feature/raw-{raw-key}-{slug}
                 注意: 如果 bug 修复同时需要实现紧相关的新功能 →
                       拆为两个 raw issue，分别 wt-create。

  --kind hotfix  紧急修复，从 main 创建，合并到 main + develop。
                 其他流程与 fix 完全一致（测试不可跳过）。
                 分支: hotfix/<desc>-<YYYYMMDD>

  选了 --kind 之后，skill:freely-test-RED-execution 会根据
  fix/feature 自动采用对应的 RED 策略。

── 创建内容 ──────────────────────────────────────────────────

  1. {prefix}/raw-{raw-key}-{slug}    ← based on --base (develop), the permanent dev worktree
  2. test-pre-merge-{raw-key}-{slug}  ← based on ①, discardable testing sandbox

Before wt-create, create the raw issue on a configured platform first:
  ./bin/freely feedback --help    (review usage, then create the raw issue)

Example:
  freely feedback --repo chatterzhao/freely --title "描述" --body "..."
  ./bin/wt-create --raw-key <returned-key> --source platform     --kind fix --slug task-mode-wait-prelaunch-gate

Legacy:
  ./bin/wt-create feature/my-task-20260307 --base develop → 
-  → 

### 4. 目录变动跟踪
如果命令脚本从 bin/ 移到了其他位置，所有调用处（shell 脚本、Python 脚本、hook、skill 文档）都要跟着改。

### 5. 关联的部署/安装流程
 时释放的模板、PATH 配置、安装文档中对命令的引用。

## 验收
- [ ] 全链路 6 个 [cmd] 节点全部有对应的 freely 子命令入口
- [ ] 所有文档和脚本中对命令的引用统一为 freely xxx 格式
- [ ] 如果发生了文件移动，所有调用处已更新
- [ ] freely --help 输出完整，每个子命令有独立 --help
