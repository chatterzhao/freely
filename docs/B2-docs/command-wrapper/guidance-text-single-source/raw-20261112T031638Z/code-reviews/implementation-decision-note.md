## Implementation Decision Note

- issue_id: I-20261112T031638Z-A
- decision: 采用「文案就地修正 + AT 全域不变量守护」，不做物理共享常量库；`raw-issue-pull` 显式传 `--project`，不改 `issue-sync` 的 ROOT_DIR 默认推导。

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