# Stacked Merge Chain

用于当前 worktree 不是直接从 `develop` 派生，而是依赖上游父分支的场景。

## 目标

输出一条显式的逐层治理链，而不是只回答“这棵树能不能 merge”：

1. `child -> parent`
2. `parent -> merge-prep-from-develop`
3. `merge-prep -> develop`
4. `cleanup after upper layer is safe`

## 输入

- 当前 child worktree
- 直接父分支 / 父 worktree
- 最终 integration target，默认 `develop`
- child / parent 各自的：
  - git cleanliness
  - pre-brainstorm / candidate / issue / milestone 状态
  - tests / review / live smoke
  - 是否存在未提交 skill / docs / runtime 产物

## 输出

1. merge chain 图
2. 每一层的 gate 结果
3. 当前真正阻塞层
4. 是否必须新建 merge-prep worktree
5. 若 merge-prep 暴露新问题，该问题归属到哪一层

## Gate Matrix

### child -> parent

- child 自己必须：
  - docs / issue / milestone / review / tests 对齐
  - worktree clean
- parent 也必须至少：
  - worktree clean
  - 没有未提交的 skill / docs / runtime 收口
- 若 parent 自己 dirty，先停在 parent hygiene，不继续往上

### parent -> merge-prep-from-develop

- parent 被 child 更新后，必须重新检查：
  - parent 自己的 docs 与 milestone 是否仍自洽
  - parent 是否仍缺 review / verification
- 若 target 是 `develop`，复杂链路默认要求新建 merge-prep worktree
- 不在 `develop` 主工位直接试合

### merge-prep -> develop

- merge-prep 的职责：
  - 合入最新 parent
  - 解 additive governance 冲突
  - 跑最小集成回归
  - 暴露 develop 面才会出现的问题

- 若 merge-prep 暴露新问题：
  - additive governance conflict：
    - 继续在 merge-prep 解决
  - real code conflict：
    - 进入 `premerge-reconcile`
  - integration bug：
    - 记为 merge-prep 阶段发现的 develop integration fix
    - 不要直接回判成 child 未完成

## 硬规则

- child 不得跳过 parent 直接并向 `develop`
- parent dirty 是上游 gate，不是旁支噪音
- merge-prep 是正式步骤，不是临时技巧
- cleanup 只能在上层也安全后进行
- 若某一层暴露新问题，应在对应层 materialize 新 issue / candidate，而不是硬顶着继续 merge
