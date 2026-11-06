# Brainstorms: raw-20261106T065711Z

## 问题

用户要求「分析各个 guarded 命令耗时是否合理」。实测 `pr-create-guarded` 347s / `pr-merge-guarded` 188s / `wt-close` 63s / `pr-review-guarded` 31s。cProfile 与分层计时证明 **约 70% 是本地 N+1 子进程，不是网络**：

| 阶段 | 实测 | 子进程 | 性质 |
|---|---|---|---|
| Step 2e 评论决议扫描 | 188s | ~4000（804 文件 × 5） | 纯本地 |
| Step 2c `governance-merge-gate` | 55s | 3423 次 git | 纯本地 |
| Step 0b `discover_raw_replicas` | 20–33s | 12–22 | 网络 |
| Step 3/4 双平台 fetch + push + PR | 30–45s | ~10 | 网络 |

`governance-merge-gate.build_issue_index()` 为索引 1522 个 issue 文件跑 `git cat-file -e` + `git show`，占该门禁 54.5s / 99%。该门禁在 pre-commit（每次 commit）、pre-push、pre-merge-commit、pr-create Step 2c、pr-merge 都会跑，一条 issue 链路累计浪费 5–7 分钟。

本机 IDE 的 `brokered-bin` shim 把基础命令从 9ms/文件放大到 248ms/文件（约 27×），但数千次子进程的设计在任何环境都不合理。

## 关键评审：证伪「改用精确搜索」

用户明确提醒「功能逻辑不要误修改，比如精确搜索是否真的符合需求」。逐条核查后**撤回该方向**：

- GitHub 端 `GitHubHandler.search_raw_issue` 本来就是精确搜索，但分别以 `in:title` 与 `in:body` 做两次 `--state all --limit 20` 服务端搜索，并客户端二次校验 needle；改 title-only 会丢掉第二次 body 搜索。
- Gitee 端无服务端 raw-key 搜索，源码注释明确要求 `--state all --per-page 100` 最多 20 页全量枚举 + 本地 title/body 匹配；单页会漏掉老副本，破坏 identity resolution 与平台 parity。
- 实测 **803/803（100%）** 的 `docs/B1-docs/raw-*/issue.md` frontmatter 含 `local_id: raw-<key>`，平台 body 继承该 frontmatter → body 匹配是主命中路径，不是边缘情况。
- `--limit 20` / 20 页上限服务于 `_resolve_raw_identity()` 的 ambiguous 判定；任意截断会把「多副本」误判成「单条兜底」。
- 同理否决：削减 `_retry_read` 3 次重试（削弱「读失败 ≠ 无 issue」fail-closed）、跨写操作缓存 remote head（读到陈旧值）、把 staged/range 视图简化成直读磁盘（违反 `read_repo_text` 优先级）。

结论：**只做两项零语义变化优化**，其余一律列为「明确不纳入」。

## 测量偏差纠正（写入正文以免后续实现者被误导）

- 一次测量误把 stdout 重定向到 `/dev/null`，引入沙箱代理开销得到 200s，非源码真实路径。精确复制源码 + 完整 `os.environ` 稳定值 187.76 / 187.69 / 188.74s。
- 另一次误用精简 PATH 绕开 IDE shim，得到 6s；本机 `brokered-bin` shim 会让每次 `python3` 启动额外 ~3.5s，每次 `open()` 额外 ~4.4ms。
- 因此性能断言必须**区分算法耗时与 I/O/解释器环境开销**：Step 2e 纯计数 0.005s、含 804 次 open 的完整扫描 3.487s、相对基线 188s 为 53.9×。

## Root Causes

1. **R1**: `pr-create-guarded` Step 2e 用 `find` + `cat` + 2× `grep -c` 逐文件循环，做的只是两个字符串计数。
2. **R2**: `governance-merge-gate` 的 `staged_path_exists` / `range_path_exists` / `read_repo_text` 每个路径各起一个 git 子进程；`path_exists` 还对同一路径重复探测，无缓存。
3. **R3（非本 issue）**: 双平台操作串行、同一链路重复 fetch develop 4–5 次、`discover_raw_replicas` 全量分页枚举——但这些都绑定 fail-closed 语义，不在本 issue 范围。

## Candidates

- **a（采纳）**: Step 2e 单进程化 + `governance-merge-gate` 批量读取。零语义变化，收益 243s / 轮。
- **b（否决）**: 改 title-only 精确搜索 / 只搜 open / 减少分页。破坏 fail-closed identity resolution。
- **c（否决）**: 削减重试、跨写缓存 remote head、简化视图优先级。改变正确性语义。
- **d（否决）**: 把性能优化与 Q2 刚收敛的 `issue-sync` / `pull_raw_issue` 标题达标逻辑合并。越界且易退化。

## 可行性预验证

- 构造样本 `grep -c "^### comment-" = 3` / `grep -c "^#### resolution-" = 2`，与 Python `startswith` 完全一致；`find` 路径集合 803 = `pathlib.glob` 803（本轮实测 804，含新物化 issue）。
- `git cat-file --batch` 实测同时接受 `:docs/milestones.md`（index）与 `82cd1e8de:docs/milestones.md`（range），且与 `git show` 字节级一致（42583B / 42583B，两者均 `identical=True`）。

## Related findings（本轮自举评审，未新建 raw issue）

- 3 个 `test-merge-guarded*` 测试恒失败（rc=13，ENOENT）：它们复制 `docs/system/workspace/scripts/worktree/merge-guarded`，但该文件已迁移；`bin/merge-guarded` 现在是 deprecated shim，实际 `exec bin/pr-merge-guarded`。属「测试与实现漂移 / 测试永久无人执行」家族，**已被 #4151（测试证据链可验证 + 替换 CI 桩，正文含 known-broken、519 个测试无人执行）覆盖**，按「只给未覆盖缺陷新建」约束不重复创建。
- 另 4 个门禁相关测试在 develop 基线同码失败，同属 #4151。证据见 AT-001-GREEN.log「7 个直接相关回归测试基线对比」。
- 本轮全部 6 项差异化输出仅为耗时数字与随机临时目录名，无语义差异。
