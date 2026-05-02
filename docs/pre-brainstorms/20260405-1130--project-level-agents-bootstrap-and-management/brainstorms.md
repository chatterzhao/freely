# Brainstorm - 20260405-1130--project-level-agents-bootstrap-and-management

## Problem

Freely 已经会在 `init` 时为托管项目补一个最小根级 `AGENTS.md`，执行时也会先读取项目根 `AGENTS.md`。但“如何生成、何时生成、是否覆盖、如何长期管理、Freely 自举时如何复用同一规则”还没有形成稳定 capability contract。

## Confirmed Facts

- `docs/system/workspace/scripts/runtime/freely` 中存在 `ensure_project_agents_md()`，并在 `init` 路径调用。
- `docs/system/workspace/scripts/tests/test-freely-init-cc-config` 与 `docs/system/workspace/scripts/tests/test-freely-init-ai-default-precedence` 已覆盖“缺失时会创建 `AGENTS.md`”。
- `docs/system/workspace/scripts/start-lead-agent.sh` 与 `docs/system/workspace/README.md` 已把项目根 `AGENTS.md` 作为第一治理入口。
- 当前高层规范只冻结了“项目根应存在可用 `AGENTS.md`”与“`AGENTS.md` 是入口，不替代高层真源”；尚未冻结模板层级、覆盖策略、演进策略。

## Boundary Judgment

- 这不是当前 `AGENTS.md` 输出风格实验的一部分。
- 这是一个潜在的 Freely 可复用能力 follow-on，应该先停留在 pre-brainstorm，而不是继续塞进现有 owner。
- 如果后续推进，真源应进入 `docs/system/**`、`bin/**`、测试与实现目录，而不是仅靠当前仓库的 `AGENTS.md` 说明。

## Key Questions

1. `freely init` 对已有项目自定义 `AGENTS.md` 的 contract 是什么：永不覆盖、可合并、还是显式交互升级？
2. 生成的默认 `AGENTS.md` 模板与 Freely 仓库自用的 `AGENTS.md` 是否属于不同层级？
3. runtime 读取项目 `AGENTS.md` 后，如何与 Freely 复用能力真源组合，而不发生职责漂移？
4. Freely 自举开发自己时，谁负责维护本仓库 `AGENTS.md`，以及它与 future generated template 的关系是什么？

## Next Routing

- 这条能力缺口现在进入独立 owner materialization。
- 第一轮 owner 只冻结 capability contract 的最小真源：capability doc、preserve-existing-AGENTS 回归测试、模板层级边界与 self-hosting 管理契约。
- 若后续需要更丰富的模板注入、升级/merge 策略或交互式迁移，再从这个 owner 继续拆 follow-on。
