# Tasks

1. 冻结 `feature/*`、`test-pre-merge-*`、`develop` 的职责边界，不再让 promote model 散落在多个旧文档和脚本假设里。
2. 明确 single-feature lane 是默认 develop-bound 讨论入口，explicit multi-bundle lane 是额外声明的组合路径，而不是第二种无约束前缀。
3. 冻结 multi-bundle 最小可追溯概念：source features、feature shas、merge order、base develop sha、stale/rebuild trigger。
4. 写清本 owner 只冻结模型，不直接承诺 `pr-merge-guarded`、hook、`governance-check`、wrapper 的具体实现。
5. 把后续工作拆成至少两个 follow-on：promotion gate enforcement、family lifecycle automation。
6. 对齐 candidate / milestone / issue 写回，让后续执行 authority 以本 owner 为准。
