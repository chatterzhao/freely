# 预研头脑风暴：manager-delegated-intake-absorption-closure

## 背景

Freely 现在已经有两层 delegated continuation 证据：

1. manager continuity / prompt / session-state 会记录某批 delegated continuation 已被当前 prompt 吸收；
2. `.freely/intake/<id>/meta.env` 则把同一批 item 长期保留在 `STATUS="delegated"`。

真实 dogfood 暴露出的现象是：

- `manager-continuity-*.md` 会反复把旧 interruption 写进 `absorbed_intake_ids`
- `live-status` 一度会把它们记成 consumed
- 但 `.freely/intake/*/meta.env` 仍保持 `delegated`
- 随着历史插话增加，表面 backlog 会不断堆积，manager 还要反复在 continuity 里解释“这些其实已经 absorb 过”

这说明当前缺的不是“prompt consumed evidence”，而是 delegated intake lifecycle 的最终闭环。

## 问题定义

需要冻结一个更清楚的 contract：

1. `manager judgement absorbed` 和 `intake lifecycle absorbed` 是否是两件事？
2. 如果是两件事，runtime 什么时候应把 delegated intake 从 `delegated` 收成 `absorbed`？
3. 什么情况下必须保留 `delegated`，以支持 restart / reentry / recovery？
4. `absorbed_intake_ids` 这个词是否继续代表治理叙述，还是应该落回 machine-readable lifecycle truth？

## 现场证据

当前实现里：

- interruption dispatcher 只消费 `STATUS=new` 的 intake，不会再次处理 `delegated`
- manager prompt build 会把本地 delegated continuation 塞回 prompt
- session-state 会写 `LAST_DELEGATED_CONTINUATION_CONSUMED_IDS`
- 但当前 prompt absorbed 并不会自动改写 intake `meta.env`

因此“已经被当前 prompt 吃进去”和“lifecycle 已闭环”被实现成了两条平行语义。

## 当前判断

当前边界已经足够稳定，可以冻结为一个新 lifecycle，而不是继续塞回已完成的 `I-20260322-0049`：

1. `I-20260322-0049` 已完成的 scope 只覆盖：
   - generated
   - consumed_into_prompt
   - pending_after_failure
2. 该 issue 自身真源已经写明：
   - 如果后续要继续扩“manager continuation 最终产出显式治理结论”的更高层语义，应通过新 lifecycle 承接
3. 当前 gap 正是这层“最终闭环语义”，因此不应 reopen 已完成 issue

## 目标

1. 为 manager-delegated intake 增加最终 absorbed closure contract
2. 定义“什么时候仍保留 delegated，什么时候必须 absorbed”
3. 让 machine-readable intake truth 与 continuity judgement 不再长期漂移
4. 保持 worker/manager 的 restart/reentry 能力，不因为过早 absorbed 而丢恢复入口

## 非目标

1. 不重写 interruption dispatcher
2. 不重写整个 intake schema
3. 不把所有 delegated intake 都一刀切 absorbed
4. 不借这条 issue 顺手改 worker-side delegated continuation 生命周期

## 候选方向

1. 最小 reconciler
   - 当 manager prompt 已消费 delegated continuation
   - 且本轮成功产出新的 manager continuity / followthrough artifact
   - 将对应 intake 显式 `resolve --status absorbed`
2. 失败轮继续保留 delegated
   - 如果本轮没有新 continuity
   - 或 manager 失败退出
   - 或当前只是 prompt 注入但没有新治理产物
   - 则保持 delegated
3. linked artifact 与 absorption target 统一
   - absorbed 后指向实际 continuity / answer artifact
   - 不再继续停留在 `pending://interruption-manager-delegation`

## 进入 IBM 前必须冻结的问题

1. 首批范围是否只限 manager-owned delegated continuation
2. absorbed 的充分条件是否必须包含“新 continuity 已成功落盘”
3. absorbed 后是否还需要保留 consumed session evidence
4. `live-status` / `baseline-status` 是否需要额外暴露新的 absorbed closure truth

## 当前收口结论

1. 这是新 lifecycle，不是 reopen `I-20260322-0049`
2. 首批只承接 manager-owned delegated continuation absorbed closure
3. 最小实现应落在 `docs/system/workspace/scripts/runtime/freely`
4. 最小验证应补到 session rotation / delegated continuation visibility 同族测试
