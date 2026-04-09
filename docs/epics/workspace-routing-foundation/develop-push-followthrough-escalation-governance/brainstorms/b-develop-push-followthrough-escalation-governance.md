# Brainstorm: develop-push-followthrough-escalation-governance

## Key Decisions

1. 这轮先 materialize 成单一 owner，而不是先拆成 `push urgency` 和 `resync trigger` 两个 owner。
2. merge 后不做 auto-push，但默认语义改为“能 push 就尽快 push”，而不是“只要可见就能长期挂着”。
3. `resync_required` 不是按固定时间猜测，而是按 owner judgment 是否依赖最新 protected truth 来判断。

## Main Tension

如果只强调 push debt 可见，AI/runtime 中断时 local-only truth 仍可能长期悬空。
如果改成 auto-push，又会把网络副作用塞进 hook/runtime，并抹掉合法的 post-merge followthrough 窗口。

因此更好的边界是：

- default: merge 后尽快 push
- exception: 只有 lawful defer 才能暂缓
- stale worktree 若继续做受最新 `develop` 影响的判断，必须先 resync

## Chosen Boundary

本 owner 只冻结四件事：

1. timely push default
2. lawful defer taxonomy
3. `resync_required` trigger
4. patrol / status surfacing contract

## Defer Taxonomy

第一版白名单应有限且可审：

- `post_merge_acceptance_in_progress`
- `cleanup_followthrough_in_progress`
- `external_remote_blocked`
- `credential_or_network_blocked`

## Expected Landing

完成后，Freely 不再把 merge 后未 push 视为“看到即可”。
系统会更明确告诉 manager：

1. 现在就该 push
2. 还是当前 defer 合法但必须保留恢复点
3. 还是某棵活跃树已 stale，必须先吸收最新 `develop`
