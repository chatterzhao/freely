# Implementation Decision Note

## Canonical landing surface

Implementation decision note 的主落点固定为当前 owner issue 的 `verification_artifact_dir` 下的 review / verification artifact。

不要：

- 新建平行 `decision-summary` 目录
- 把同一份 note 再复制到 `progress`、`prd.md`、`tasks.md`

其他产物可以引用该 note，但不能宣称自己是主真源。

## When required

当 develop-bound worktree materialize capability / implementation truth 时，默认需要 implementation decision note。

首批实现类路径至少包括：

- `bin/`
- `docs/system/`
- `src/`

不强制的典型情况：

- pre-brainstorm / candidate-only 研究
- IBM-only 文档收敛
- 纯 milestone queue / progress / review verdict writeback
- 纯 wording / formatting / rename 且未触达 capability truth

## Minimum fields

在 review artifact 中写：

```md
## Implementation Decision Note

- decision: `...`
- why_this: `...`
- alternatives_considered: `...`
- boundary_non_goals: `...`
- residual_risk: `...`
```

字段语义：

- `decision`
  - 这批实现到底选了什么方案
- `why_this`
  - 为什么在当前 owner 边界和当前批次里选这个
- `alternatives_considered`
  - 至少写出被拒绝、延后或未采用的主要替代
- `boundary_non_goals`
  - 当前不解决什么，哪些边界故意保持不动
- `residual_risk`
  - 还有什么不确定、已知风险或 follow-on

## Authoring rule

这份 note 承接的是 dev-loop decision。

它可以引用：

- 上游 candidate 的 `decision_reason`
- issue / PRD 的 `Non-Goals`
- issue-bound brainstorm 的关键结论

但不要把这些上游产物重新抄写一遍。
