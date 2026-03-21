# Issue Materialization Checklist

## Entry checks

- 当前输入已经是 milestone-owned issue，或 candidate 已被 milestone 接纳
- 若仍只是未绑定 milestone 的 pre-brainstorm candidate：回到 `doc-pre-brainstorm-execution`

## Stable ownership required

写 IBM 正式产物前，必须先确认：

- `epic-name`
- `story-name`
- `issue-name`

任一未稳定：

- 停止写正式 IBM 产物
- 回到 `doc-pre-brainstorm-execution`

## Required artifacts

- `docs/epics/{epic-name}/{story-name}/issues/{issue-name}.md`
- `docs/epics/{epic-name}/{story-name}/brainstorms/b-{issue-name}.md`
- `docs/epics/{epic-name}/{story-name}/prd.md`
- `docs/epics/{epic-name}/{story-name}/pre-tests.md`
- `docs/epics/{epic-name}/{story-name}/tasks.md`

写完后仍需按 [prd-quality-bar.md](prd-quality-bar.md) 检查 `prd.md` 是否达到 AI-ready 最小结构；未达标时不得宣称 `done_ibm`。

## Required write-back

- `candidates.md.promoted_issue_path`
- `docs/milestones.md.issue_path`
- `phase_state=in_ibm`
- 继承有效 `session_refs`
