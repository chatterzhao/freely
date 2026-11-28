## 0. 设计意图审计（先于方案）
### B0 前置：关键词广搜 + 多文档交叉
- 关键词族表：`package-runtime-file-parity` / `runtime-file-parity` → `docs/system/workspace/scripts/quality/package-runtime-file-parity.py`、`bin/freely-package:157`；`commands.md` / `不随包发布` → `docs/system/workspace/package-allowlist.txt:49-51`、`docs/B1-docs/raw-20261106T100938Z/brainstorms.md`；`command_name_contract` → `docs/system/workspace/scripts/quality/command_name_contract.py`、`docs/system/workspace/scripts/tests/test-command-name-contract.py`。
- 怀疑多份文档：是。打包真源在 allowlist 与其评审文档；R59 新能力在 quality/；不能只读 R59 注释判断是否需要扩包。
- 三类分层：当前生效实现 = `package-allowlist.txt` + `package-runtime-file-parity.py`；历史局部文档 = R59 新增的 quality checker；当前权威恢复点 = raw-20261106T100938Z 的设计判决（commands.md 不随包发布）。
- 矛盾清单：parity 检查器把 quality/ 全部当运行时消费者，而 R59 checker 只被 tests/ 调用；bin/freely 注释写入不随包发布的文档字面路径。二者均与本轮之前的打包设计冲突。
- 二元决策：**继续**——修 R59 引入的脱线，不改 parity 判据、不扩 allowlist。
### 外部锚点（引用原文）
- 设计文档: `package-allowlist.txt:49-51`「3 个纯文档/测试资料（commands.md / ...）经评审不随包发布」。
- 既有门禁源码注释: `package-runtime-file-parity.py`「Tests and B1/B2 governance docs are NOT runtime consumers」。
- 既有同类实现: `docs/system/workspace/scripts/tests/` 下的测试脚本均不进 RUNTIME_DIRS。
- 判定：实现偏差——R59 把测试期工具放错目录，并在入口注释写入非打包文档路径。
- 与既有断言的冲突：有。把 commands.md 加入 allowlist 会直接冲突 raw-20261106T100938Z；必须改调用/位置，不改门禁。
- 影响面：bin/freely 注释、checker 所在目录、AT 与函数级单测的引用路径。

## 0.1 全局适配反思（四问）
- Q1 流程能力（打包真源与测试工具边界）。
- Q2 与 package-allowlist 共享真相源；parity 拥有最终判定。
- Q3 若扩 allowlist 会产生第二份打包判决，反设计，排除。
- Q4 门禁测的是「运行时字面引用是否随包」；本轮维度是「测试工具误入运行时目录」，先修位置与引用，不放宽门禁。

## 1. 决策
Option B：入口注释去路径 + checker 移到 `scripts/tests/`；Option A（扩 allowlist）排除；Option C（放宽 parity）排除。
## 2. Candidate
C-20261128T065937Z-A promoted → M-20261128T065937Z-A。
