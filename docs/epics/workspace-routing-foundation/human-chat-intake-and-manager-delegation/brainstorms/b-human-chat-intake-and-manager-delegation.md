# IBM Brainstorm: human-chat-intake-and-manager-delegation

## Goal

把 human chat intake 的既有 runtime / skill / test 能力，收敛成正式 issue-bound 产物，确保 Freely 能把人类插话当作可恢复、可监督、可委派的正式输入面。

## Decisions

1. human chat 的默认站位仍然是 side input，不是阻塞主 loop 的同步 gate。
2. manager 负责 `notice -> claim -> choose reaction -> delegate -> absorb`，不负责深度解释。
3. `skill:human-interruption-handling` 负责解释插话、生成 resolution artifact，并给出 canonical absorption 建议。
4. `freely intake chat`、durable intake artifact、manager queue scan、resolution artifact 和 completion signal 必须一起出现，才算闭环。
5. discovery 类输入继续进入 `doc-pre-brainstorm-execution`，但必须先经过 durable intake / classification / delegation。
6. UI 若后续存在，只能复用同一 intake 能力，不得绕过 CLI 入口。

## Open Questions

1. 是否需要再拆一层专门的 interruption worker delegation flow。
2. reaction mode 的更细分文案是否要继续保留在 runtime prompt 内，还是收敛到单独的 reference 文档。
3. `.freely/run/interruption-resolution/**` 是否需要进一步标准化目录结构。

## Current Route

- 这条能力线已经在 runtime / skill / test 上形成闭环，因此当前 IBM 只负责把它 materialize 成正式 issue-bound 产物。
- 下一步进入 issue 级 verification，确认文档、milestone、测试与回流记录一致。
