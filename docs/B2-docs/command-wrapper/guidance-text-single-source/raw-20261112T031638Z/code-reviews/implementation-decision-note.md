## Implementation Decision Note

- issue_id: I-20261112T031638Z-A
- decision: 采用「文案就地修正 + AT 全域不变量守护」，不做物理共享常量库；`raw-issue-pull` 显式传 `--project`，不改 `issue-sync` 的 ROOT_DIR 默认推导。
- why_this: 单源性由**断言**保证而非物理共享——任何载体写错已退役 skill 名或漏掉必填 `--kind` 都会判红，与 R33 已建立的「AT 守护不变量」范式一致；同时把 `--project` 一处传参即可修好调用路径，符合 `issue-sync:116` 注释本就规定的用法。
- alternatives_considered: (1) 新建共享 `guidance.sh` 文案库——四个载体形态不同（shell dispatcher / Python 门禁 / 27k 行单体 / Markdown 模板）无法共享同一 shell 常量，强行做需引入生成器并新增投影种类；(2) 只逐处替换字面量、不扩断言——正是 R33 的做法，已被本轮证伪会再次漏网；(3) 给已退役名造 skill alias——等于撤销 2026-06-29 的退役决策，是真正的回退；(4) 改 `issue-sync` 的 ROOT_DIR 默认值——影响 14 个 `issue-sync.d/*` 模块与所有调用方，blast radius 过大；(5) 在 develop 上跳过 `issue-sync create`——会把 title 归一化缺口变成静默行为；(6) 把 protected guard 降级为 WARN——削弱门禁，违反铁律。
- boundary_non_goals: 不清理死代码 `task-lifecycle-scan.bak.py`；不改两处测试 fixture 的任意字符串字段值；不改 `commands.md`（`--skill` 未废弃）；不造 skill alias、不恢复任何已退役 skill；不删任何 guard 提示段落；不重构 `issue-sync` 的 ROOT_DIR 推导机制；不改 `wt-create` 的 cd 逻辑。
- residual_risk: ①端到端 `wt-create` 因 `bin/worktree-common.sh:17` 把 ROOT_DIR 重绑主仓，修复须合并后才生效，B3b 只能在合并后补证（已标 SKIP 并在合并后验证）；②文案字面仍有多处重复，正确性由 AT 守护，新增载体若未纳入扫描域仍可能漏网（已把扫描域写成「活代码 + 指定文档」，并新增反向断言防白名单滥用）；③R33.5 的 AT 改为断言「0 failed 且 >=22 ok」而非精确计数，若将来 CI 子集被大规模裁剪，该断言不会报警（由该校验自身的 S8「未删既有项」兜住）。

### 为什么不做物理单源常量库

四个载体形态不同（shell dispatcher / Python 门禁 / 27k 行 shell 单体 / Markdown 模板），
无法共享同一 shell 常量；强行做需引入生成器并新增投影种类（进 projection.lock），
改动面远超本轮。单源性改由 **AT 断言**保证：任何载体写错幽灵名或漏 `--kind` 都判红。
这与 R33 已建立的「AT 守护不变量」范式一致。

### 为什么白名单是安全的

白名单只含三类：① AT 自身的黑名单常量（必须列出幽灵名才能检测）② 死备份
（全仓零引用 + 打包时删除）③ 测试 fixture 的任意字符串字段值（被测代码不校验
skill 存在性）。AT 额外断言白名单路径均真实存在，且**四个必修项不得出现在白名单**，
防止用白名单掩盖真缺陷。

### 为什么改 Test 6 的方向而不是删掉它

Test 6 原断言「guard 必须含幽灵名才 PASS」，把历史错误固化成了判据；且用 BSD grep
不支持的 `\|`，在 macOS 上恒 NO MATCH（本轮实测）。删掉会失去「guard 必须引用 skill」
这条有价值的检查，故改为反向断言 + `grep -E`，并把这个当前不在 CI 里的测试加入 CI。

### 为什么 C-B 只加一个参数

`issue-sync:116` 的注释本身就规定了正解（`--project`）。改 ROOT_DIR 默认值会影响
14 个 `issue-sync.d/*` 模块与所有调用方；跳过 create 会把 title 归一化缺口变成静默
行为；降级 guard 违反铁律。一处传参是最小且语义正确的修法。

### 刻意不做

不动 `.bak.py`、两处 fixture、`commands.md`；不造 skill alias；不删 guard 提示；
不改 `--skill` 解析逻辑；不放宽任何门禁判据。