# 预研头脑风暴：test-lane-routing-and-enforcement

## 背景

上一条 owner 已把 `develop` 的正常 promote source 切换为 `test-pre-merge-*` family，并把测试 lane 写回 `AGENTS.md`、`LAWS.md` 和技能参考。

但实际仓库里又暴露出新的治理缺口：

1. `./bin/test-lane` 已经出现实现雏形，却没有正式 owner 链路。
2. `feature-local` 当前只校验“不是 protected branch”，这会把任意 ad hoc 分支误判为合规测试 lane。
3. 新入口文件没有执行位，文档要求的 `./bin/test-lane` / `./bin/test-test-lane` 直接失败。
4. 仍有部分技能 / checklist / hook README 继续描述旧 replay-only promote 语义。

这说明问题已经不是“提示词建议如何跑测试”，而是需要一个独立 owner 来冻结 lane contract，并把它接到 machine enforcement。

## 为什么不能继续挂在 1805 owner 下

`I-20260405-1805-A` 的 scope 是：

1. `test-pre-merge-* -> develop` source semantics
2. protected-branch promotion gate
3. 与 merge source semantics 直接耦合的 regression tests

而 `test-lane` 要解决的是：

1. 测试命令必须显式声明 lane
2. lane 与 branch/worktree 职责必须匹配
3. 包装入口、帮助文本、技能和回归必须保持一致

这和 promotion gate 相邻，但不是同一能力面。继续混在 1805 owner 里，只会让 scope 漂移。

## 初步结论

应新开独立 owner，负责：

1. 冻结三条 canonical lane：
   - `feature-local`
   - `premerge-integration`
   - `post-merge-followthrough`
2. 冻结 lane 与 branch family 的匹配关系。
3. 落地 `./bin/test-lane` 的 machine enforcement。
4. 修复可执行入口与 focused regression。
5. 对齐 `AGENTS.md`、`LAWS.md`、skills 和 references 的 lane 语义。

## 明确不做

这条 owner 不解决：

1. 自动推断 lane
2. 自动创建 `test-pre-merge-*` batch
3. batch lifecycle automation
4. runtime/fleet-status 的 lane 可视化
5. test command catalog 或统一测试编排 DSL
