# Implementation Decision Note
- issue_id: I-20261110T084522Z-A
- issue_path: docs/B2-docs/runtime/daemon/raw-20261110T084522Z/issues/I-20261110T084522Z-A.md
- decision: 新增自动扫描 lint 作为状态键契约，按实测补齐 `ALLOWED_KEYS` 77 → 142；不改未知键拒绝语义、不改任何调用点
- why_this: 白名单注释宣称「全量扫描」但实测漏 65 个键 / 3 种写入形态；`read_state` 对每行都校验键，一个未登记键让整份存量状态文件抛错，shell 侧 `|| true` 吞错后值静默回落默认值 —— 比报错更危险，且会阻塞后续所有大族迁移。
- alternatives_considered: ①只补 issue 报的 21 键——漏 44 键与 3 种形态，下次仍撞；②放宽 legacy 行的键校验——削弱「防止拼错静默产生新状态」的护栏，且读写语义不一致，issue 明确否决；③删掉白名单接受任意键——等于取消契约；④lint 只告警不失败——不会被人当真；⑤用 `git grep` 手工清单代替可执行抽取器——无法验证扫描器自身是否漏判。
- boundary_non_goals: 不改 `read_state` / `write_state` 语义；不改协议接口；不改 `runtime/freely` 任何一行；不动 `check-state-file-sources`（计数仍 52）；不动三族已迁调用点；不删除既有状态文件；不做逐族迁移（那是 R23.14 起的工作）。
- residual_risk: ①lint 的抽取器是启发式的，新增第 6 种写入形态需同步扩充并加夹具；②stale 只告警不失败，临时移除写入点后白名单可能残留（review 可查）；③小写锁状态键纳入白名单后，`read_state` 也能读它们，但这些锁文件目前仍走专用 snapshot 函数，尚未验证端到端；④`--kv` 形态依赖字符串 `--kv "KEY=`，若将来改用 `--data` JSON 需扩充抽取器。
- verification: AT-001 基线 RED `1 ok / 15 failed`（唯一 PASS 是「未知键仍拒绝」）→ 工位 GREEN `16 ok / 0 failed`；lint missing=0 / stale=0；三族 AT + 10 个相关测试 + `test-all --ci` + 两个 lint 全绿。
- self_bootstrap_findings: ①issue 报 21 键 / 2 种形态，实测 65 键 / 5 种形态；②**扫描器自身漏判两次** —— heredoc 目标用 `[^"\s]*` 匹配不到 `cat >"$(fn "$project")" <<EOF`（漏 15 键），改用 `.*<<` 后又把 `<<<` 当 heredoc、把 here-string 载荷里的局部变量误当状态键（多 7 个）；修法是 here-string 优先 + `(?!<)` 排除；(3) 由此确立「扫描器必须有独立夹具测试」，否则 lint 通过只是自证；④`--kv` 写入点必须纳入抽取器，否则已迁的两族会产生 6 个假 stale。

## Implementation Decision Note
- decision: 自动扫描 lint + 补齐 65 键 + 扫描器夹具
- why_this: 兼容读取旧格式会整份抛错且被吞成静默丢状态
- alternatives_considered: 只补 21 键 / 放宽 legacy / 取消白名单 / 只告警 / 手工清单
- boundary_non_goals: 协议语义、调用点、freely、既有状态文件、逐族迁移均不动
- residual_risk: 启发式抽取器、stale 只告警、小写锁键未端到端、--kv 字符串依赖
