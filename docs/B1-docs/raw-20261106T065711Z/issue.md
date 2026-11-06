---
schema_version: '1'
local_id: raw-20261106T065711Z
kind: raw
phase_state: absorbed
absorbed_into: I-20261106T065711Z-A
platform_ids:
  github:
    issue_id: '4198'
    url: https://github.com/chatterzhao/freely/issues/4198
    synced_at: ''
  gitee:
    issue_id: IKTF7Y
    url: https://gitee.com/zhaoquan/freely/issues/IKTF7Y
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-11-06T06:57:11Z'
updated_at: '2026-11-06T07:41:59Z'
intake_id: ''
author: platform
channel: github
session_refs: []
platform_state: closed
promoted_children: []
source_candidate: ''
completed_at: '2026-11-06T07:41:59Z'
closeout_note: ''
---

# perf: 批量化治理门禁读取，消除 N+1 子进程开销

workflow_kind: feature

## 优先级

P1 — 不阻断正确性，但每条 issue 完整治理链被纯本地门禁浪费 5–7 分钟，1000 轮自动化累计不可接受，且容易被误判成「平台网络抖动」而掩盖真实瓶颈。

## 不退化边界（本 issue 的前提，逐条实证）

本 issue 只做**零语义变化的纯性能优化**。以下既有逻辑必须保持不变，不得「顺手优化」：

1. `platform-adapter.py` 的 `search_raw_issue()` 双平台搜索契约：
   - GitHub 端已经分别以 `in:title` 与 `in:body` 做两次 `--state all --limit 20` 服务端搜索，并在客户端二次校验 needle；改成 title-only 会直接丢掉第二次 body 搜索。
   - Gitee 端无服务端 raw-key 搜索，源码注释明确要求 `--state all --per-page 100` 最多 20 页全量枚举 + 本地 title/body 匹配；单页会漏掉老副本，破坏 identity resolution 与平台 parity。
   - 实测 803/803（100%）的 `docs/B1-docs/raw-*/issue.md` frontmatter 含 `local_id: raw-<key>`，平台 issue body 继承该 frontmatter，**body 匹配是主命中路径而非边缘情况**。
   - `--limit 20` / 20 页上限服务于 `_resolve_raw_identity()` 的 ambiguous 判定；任意截断会把「多副本」误判成「单条兜底」。
   - 因此「改成按 title 精确搜索」「只搜 open」「减少分页或 limit」全部禁止。
2. `_retry_read()` 的 3 次重试 + jitter backoff 与 fail-closed 语义（平台不可读 ≠ 没有 issue）不得削减。
3. `governance-merge-gate.read_repo_text()` 的视图优先级：staged view（`git show :path`）→ range view（`git show REF:path`）→ 磁盘；源码注释说明 range 必须优先于磁盘（源分支文件不在目标工位磁盘上）。`FileNotFoundError` 语义不变。
4. `guarded_pr_update` 对每个平台分别 `fetch_branch_head`；跨写操作不得缓存 remote head，否则读到陈旧值。
5. `bin/issue-sync._platform_title()`、`platform-adapter.pull_raw_issue()` 的标题达标与身份逻辑不在本 issue 范围（Q2 刚收敛，禁止再动）。

## 根因

两条**纯本地**路径存在 N+1 子进程爆炸，与网络无关：

- `pr-create-guarded` Step 2e（评论决议扫描）：`find` + `cat` + 2 次 `grep -c` 对 803 个文件循环，约 4000 个子进程，做的只是两个字符串计数。
- `governance-merge-gate.build_issue_index()`：为每个 issue 文件跑 `git cat-file -e`（`range_path_exists` / `staged_path_exists`）与 `git show`（`read_repo_text`），共 3423 次 git 子进程；`path_exists()` 还对同一路径重复探测，无缓存。

本机 IDE 的 `brokered-bin` shim 把基础命令从 9ms/文件放大到 248ms/文件（约 27 倍），但「数千次子进程」这个设计本身在任何环境都不合理。

## 证据（本轮实测）

| 项 | 实测 | 来源 |
|---|---|---|
| `pr-create-guarded` 整条 | 347s | Q2 轮次计时 |
| Step 2e（精确复制源码 + 完整环境） | 187.76 / 187.69 / 188.74s（3 次） | bash 循环 |
| 同语义单进程 Python 等价实现 | 0.22s | `pathlib.glob` + `startswith` |
| `governance-merge-gate --range` | 55.01 / 55.34s（2 次） | 真源命令 |
| cProfile 热点 | `build_issue_index` 54.5s（占 99%）；`parse_issue_file` 1522 次；`subprocess.run` 3423 次（`git show` 1538 + `cat-file -e` 1885） | `python3 -m cProfile -s cumulative` |
| 该门禁调用点 | pre-commit（每次 commit）、pre-push、pre-merge-commit、pr-create Step 2c、pr-merge | 源码 grep |
| 网络基线 | GitHub `ls-remote` 4.96–5.63s、Gitee 1.59–1.86s、`gh api` 1.03–1.11s、`discover_raw_replicas` 20–33s | 分层计时 |

等价性与可行性已预先验证：

- 构造样本上 `grep -c "^### comment-" = 3` / `grep -c "^#### resolution-" = 2`，与 Python `startswith` 计数完全一致；`find` 路径集合 803 = `pathlib.glob` 803。
- `git cat-file --batch` 实测同时接受 `:docs/milestones.md`（staged/index）与 `82cd1e8de:docs/milestones.md`（range），因此批量化方案可行。
- 一次测量曾因误把 stdout 重定向到 `/dev/null` 引入沙箱代理开销而失真；上表均为精确复制源码、完整执行环境下的稳定值。

## 影响

- 每条 issue 的完整链路本地门禁累计浪费 5–7 分钟；`pr-create-guarded` 347s 中约 243s 是这两项。
- 真实网络 RTT 只有 60–90s，却被本地进程开销掩盖，排障时容易误判为 GitHub 抖动。
- 优化后预期 `pr-create-guarded` 降到 90s 以内（剩余为双平台真实网络 RTT）。

## 修复方案（仅纯性能优化）

1. **Step 2e 单进程化**：改为一次 Python 扫描遍历 `docs/B1-docs/raw-*/issue.md`，用 `startswith("### comment-")` / `startswith("#### resolution-")` 计数，保持 `_unresolved > _resolved` 的判定与原有报错文案、原有文件集合。
2. **governance-merge-gate 批量读取**：
   - 一次性 `git ls-tree -r --name-only <REF>` 建立 range 路径集合；一次性 `git ls-files -s`（或 `cat-file --batch-check`）建立 staged 路径集合，替代逐路径 `cat-file -e`。
   - 用单个 `git cat-file --batch` 进程读取 `:path` 与 `REF:path`，替代 1538 次 `git show`。
   - 对 `range_path_exists` / `staged_path_exists` / `path_exists` 加进程内缓存（键 = 视图 + 路径）。
   - **严格保持** staged > range > disk 优先级与 `FileNotFoundError` 语义，补三视图优先级行为测试。
3. **可选低风险项**：同一条命令内对同一 `raw_key` 的重复 `discover_raw_replicas` 只读结果去重；不得跨写操作缓存，不得改动搜索字段、状态范围、分页或重试。

## 明确不纳入（已评审否决，禁止夹带）

- 把 `search_raw_issue` 改成 title-only 精确搜索、限定 `--state open`、减少分页或 `--limit` —— 会漏掉 body-only 命中与 closed 副本，破坏 fail-closed 的 identity resolution 与 ambiguous 判定（见不退化边界 1）。
- 削减 `_retry_read` 的重试次数或退避 —— 削弱「读失败 ≠ 无 issue」语义。
- 跨写操作共享或缓存 `git fetch` 结果、remote head —— 会读到陈旧值。
- 把 staged/range 视图简化成直读磁盘 —— 违反 `read_repo_text` 既有优先级。
- 修改 `issue-sync`、`pull_raw_issue`、门禁判定规则或标题达标逻辑 —— 越界，且属 Q2 刚收敛的能力，禁止退化。

## 验收标准

- GREEN：Step 2e 单进程版对 803 份真实 issue.md 及构造样本，`unresolved` / `resolved` 计数与最终判定逐文件与旧实现一致。
- GREEN：`governance-merge-gate` 对同一 `--range` 与同一 `--staged` 输入，优化前后 verdict、warning、退出码完全一致；新增 staged / range / disk 三视图优先级行为测试。
- GREEN：`discover_raw_replicas` 的 matches 集合、ambiguous 判定、closed 副本可见性与优化前一致（用 body-only 命中样本验证）。
- GREEN：`build_issue_index` 的 git 子进程数从 3423 降到个位数；Step 2e 从 188s 降到 1s 内。
- GREEN：整条链路实测 `pr-create-guarded` 从 347s 降到 90s 以内。
- 禁止：不得为减少子进程而删除任何视图分支、搜索字段、状态范围或重试逻辑。
