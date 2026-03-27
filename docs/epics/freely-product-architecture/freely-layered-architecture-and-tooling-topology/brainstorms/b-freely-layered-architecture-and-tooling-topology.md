# IBM Brainstorm: freely-layered-architecture-and-tooling-topology

## Key decisions

1. 当前 scope 是 Freely 自身产品/系统架构，不是 Freely 能力目录扩写。
2. 首个正式产物先回写：
   - `docs/PROJECT_INTENT.md`
   - `docs/CONSTITUTION.md`
   - `docs/LAWS.md`
   - `AGENTS.md`
3. `AGENTS.md` 只负责“开发 Freely 时怎么判断落点”，不负责定义架构本体。
4. `docs/system/workspace/**` 与 `tools.md` 仍是能力真源，只作为局部证据输入本 issue，不是本 issue 的直接落点。

## Frozen terminology

- `Freely product`
- `Freely core`
- `Freely CLI`
- `Freely TUI app`
- `Freely GUI app`
- `host shell`
- `semantic surface`
- `external AI tooling layer`

## Core mapping

- `Freely core`
  - runtime / orchestration
  - service contract / adapter boundary
  - external AI tooling orchestration
  - eval / harness / operational substrate
- `Freely CLI`
  - Freely core
  - CLI command set
- `Freely TUI app`
  - Freely core
  - TUI shell
- `Freely GUI app`
  - Freely core
  - GUI shell

## Semantic surfaces

这些不是 shell peer：

- `init`
- `start`
- `chat`
- `baseline-status`
- `live-status`
- `fleet-status`

它们通过 `CLI shell`、`TUI shell`、`GUI app` 等 host shell 暴露，但本身属于 command / submit / observability semantics。

## Guard rails

- 不把 Freely 当前的 `CLI-first` 直接泛化成未来任何产品都该遵循的能力
- 不把“正式文档”误写成“能力真源”
- 不把外部 AI tool 误当成 Freely 自己的 product shell
