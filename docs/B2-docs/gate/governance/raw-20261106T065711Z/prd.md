# PRD: 批量化治理门禁读取，消除 N+1 子进程开销

- issue_id: I-20261106T065711Z-A
- source_raw: raw-20261106T065711Z
- workflow_kind: feature
- milestone: M-20261106T065711Z-A
- story: gate/governance（复用既有 story，epics-map.svg 无需改动）

## 目标

在不改变任何门禁判定语义的前提下，把治理门禁的纯本地 N+1 子进程去掉，让每条 issue 的完整治理链少等 5–7 分钟。

## 背景与不退化边界

用户要求「功能逻辑不要误修改，比如精确搜索是否真的符合需求」。已逐条证伪并写入 B1 brainstorms。本 PRD 的**唯一**改动范围：

1. `pr-create-guarded` Step 2e 评论决议扫描的执行方式（循环 → 单进程）。
2. `governance-merge-gate` 读取 git 对象与探测路径存在性的执行方式（逐路径 git 子进程 → 一个持久批量进程 + 缓存）。

必须保持：
- `read_repo_text` 视图优先级 staged（`:path`）> range（`REF:path`）> disk；`FileNotFoundError` 文案逐字节不变。
- `path_exists` = disk OR staged OR range。
- Step 2e 文件集合 `docs/B1-docs/raw-*/issue.md`、`^### comment-` / `^#### resolution-` 行计数、`unresolved > resolved` 判定、输出行格式（含 em dash）、失败块文案与退出码。
- `search_raw_issue` 双平台搜索字段 / `--state all` / 分页 / `--limit 20` / 客户端二次校验；`_retry_read` 3 次重试；`guarded_pr_update` 每平台独立 fetch；跨写操作不缓存 remote head。

## 用户故事

作为 freely 的使用者与自动化执行者，我期望每次提交与 PR 的门禁在秒级完成，而不是把真实网络 RTT 埋在数千次本地进程里，导致排障时误判为 GitHub 抖动。

## 功能需求

- FR-1: 新增 `docs/system/workspace/scripts/quality/comment-resolution-scan.py`，单进程完成 Step 2e 扫描；输出格式与旧 shell 循环一致；缺文件时 `pr-create-guarded` fail-closed 而不是静默跳过。
- FR-2: 新增 `docs/system/workspace/scripts/quality/governance_repo_view.py`，提供 `RepoView`；一个长驻 `git cat-file --batch` 进程、按 spec 缓存、支持 `:path` 与 `REF:path`；非 blob / 无法解析时回退到原单次 `git show` / `git cat-file -e`，保证边界行为不变。
- FR-3: `governance-merge-gate` 的四个函数（`staged_path_exists` / `range_path_exists` / `read_repo_text` / `path_exists`）委托 `RepoView`，但分支优先级与返回语义完全不变；`atexit` 关闭批量进程。
- FR-4: `read_repo_text` 经批量读取时仍应用 universal newline 与严格 UTF-8 解码，与 `subprocess.check_output(text=True)` 一致。
- FR-5: 新增回归测试 `test-governance-gate-batch-read`，四组（static / unit / equivalence / perf），含三视图优先级行为测试与子进程计数断言。

## 非功能需求

- NFR-1: `build_issue_index` 的 git 子进程数从 3423 降到个位数。
- NFR-2: `governance-merge-gate --range` 同输入 verdict byte-identical，耗时降至秒级。
- NFR-3: Step 2e 不再有进程扇出；纯计数逻辑保持亚秒。
- NFR-4: 对 4,363 份真实治理文档双视图逐函数新旧对比 0 差异。
- NFR-5: 相关回归测试零新增失败。

## 明确不纳入

title-only 精确搜索、限定 open、减少分页/limit、削减重试、跨写缓存 remote head、简化视图优先级、改动标题达标逻辑与门禁判定规则。

## 验收

见 `verification/pre-tests.md` 的 AT-001 与 `verification/test-evidence/AT-001-RED.log` / `AT-001-GREEN.log`。
