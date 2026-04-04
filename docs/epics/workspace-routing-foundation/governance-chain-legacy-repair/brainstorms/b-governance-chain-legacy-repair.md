# Brainstorm: governance-chain-legacy-repair

## Boundary

这条 owner 不是“给 develop 一次性放行”，而是把已经存在于 canonical 历史里的治理链断裂重新收回到一个合法 lifecycle 下。

它要回答的核心问题有三类：

1. 哪些 drift 是历史遗留 truth 缺口
2. 哪些 historical repair slices 只是 parent owner 的 implementation decomposition
3. 如何在不降低 gate 严格度的前提下恢复 canonical chain

## Historical Repair Slice Map

### umbrella owner

- `20260403-1100--governance-chain-legacy-repair`

### historical child repair slices

- `20260403-1200--verification-artifact-dir-repair`
- `20260403-1201--implementation-decision-note-repair`
- `20260403-1202--candidate-touched-repair`
- `20260403-1203--issue-id-key-repair`

这些子切片的共同特征是：

- 都由同一轮 `governance-merge-gate` 收紧触发
- 都在回答“如何把 legacy truth 补到当前规范”
- 当前都已不在现有文件系统中，因此不能再被当作 active lane

因此它们不应再伪装成已经独立 materialized owner，而应作为 historical child slices 被 parent owner 吸收并留痕。

## Option Space

### Option A: weaken the gate

优点：
- 最快解除表面阻塞

缺点：
- 直接违反这次 repair 的出发点
- 会让未来继续把 legacy drift 推进进来

### Option B: recreate one issue per historical child slice immediately

优点：
- 每条 repair slice 都有自己完整 owner

缺点：
- 当前 parent owner 还没 materialize，会先把治理链继续拆散
- 对这批显然同源的问题过度建模

### Option C: materialize one umbrella owner first, then absorb or legalize child slices

优点：
- 先恢复 canonical authority
- 允许 child lanes 作为 implementation decomposition 存在
- 最符合当前真实依赖关系

缺点：
- 需要 parent owner 明确记录 child-slice relationship

## Decision

实际已执行 Option C，并在 closeout 中把 parent owner 写回历史完成态：

1. 让 `1100` 成为本次 legacy governance-chain repair 的 canonical owner
2. 要求 `1200/1201/1202/1203` 不再以 active slice 身份出现在 canonical docs 中
3. 对每个 child slice 做二选一：
   - absorbed into `I-20260403-1100-A`
   - or later materialize a real issue/progress chain

## Non-Negotiables

- 不能用 gate weakening 替代 legacy repair
- 不能继续让 promoted candidate 指向不存在的 issue
- 不能让 sibling worktree 关系只存在于 commit message 里，而不写进 canonical docs
- 不能在 closeout 后继续把 `1100` 叙述成 current umbrella owner
