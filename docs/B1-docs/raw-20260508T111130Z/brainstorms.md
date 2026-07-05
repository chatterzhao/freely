# Brainstorm: reference-transaction hook delete 拦截

- 来源: raw-20260508T111130Z30Z (#256)
- 日期: 2026-05-08

## Discovery

`git branch -d test-pre-merge-*` 删除已合并分支时被 reference-transaction hook 拦截，报 "Branch creation blocked"。

## Research

Hook 在 `while read old_oid new_oid refname` 循环中收到 aborted 事务时，`old_oid=000... new_oid=000...`（两者都为零）。第 50 行 `if [[ "$old_oid" == "$zero_oid" ]]` 将其误判为 branch creation 并拦截。

Git reference-transaction hook 对每个事务调用多次（aborted + prepared + aborted）。aborted 阶段两个 oid 都为零。

## Decision

在 creation guard 之前加 aborted/no-op 事务跳过检查：`if [[ "$old_oid" == "$zero_oid" && "$new_oid" == "$zero_oid" ]]; then continue; fi`
