# Brainstorm: develop-merge-issue-binding-and-cmi-governance

## Goal

把 develop merge gate 从“仓库里存在 candidate / owner issue 就算有治理痕迹”收紧为“本次 merge 明确绑定具体 issue，且 touched candidate 与 touched owner issue 必须同线”。

## Key Decisions

1. owner 证据必须进入同次 diff，不能靠仓库里的静态存在放行
2. `promoted` 与 `absorbed` 都要验证 owner issue 是否同次进入 diff
3. unrelated issue 不能替别的 candidate 充 owner
4. focused regressions 直接覆盖 borrowed owner issue

## Non-Goals

- 不在本批次重写所有历史 `absorbed` 候选
- 不把 milestone phase rule 一次性扩成全仓审计器
- 不顺手修所有旧 issue id/key 的历史债

## Outcome

这条 gate 修完后，develop merge 至少要满足两层：

1. 有具体 owner issue/progress/review
2. owner 与 candidate 在同一条 `C/M/I` 线上
