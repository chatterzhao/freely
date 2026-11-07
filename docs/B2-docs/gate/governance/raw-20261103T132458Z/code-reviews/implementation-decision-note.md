# Implementation Decision Note
- issue_id: I-20261103T132458Z-A
- decision: 统一退出码 0/1/2，把 6 个 shim / pre-commit.sh / pr-create-guarded / checkpoint-guard / check-file-size 的「环境缺失即通过」全部改为 fail-closed，同时精确保留 3 类合法路径
- why_this: 门禁存在性与有效性脱钩时，一次丢执行位或一次 zip 解包就能静默关掉全部客户端门禁，且日志里与真实通过不可区分。这是 R9/R10 等后续门禁修复的可信度前置。
- alternatives_considered: 无差别改整族 shim（会阻断 `git worktree add` 触发的 post-checkout，自锁每轮 wt-create）；把外部项目也判为环境故障（误伤全部外部项目）；把 check-file-size 全量结果直接阻断 commit（历史 7 个 ERROR 会让每轮提交必挂）；把「no raw key」也改成失败（破坏合法路径）；给 `.githooks/bin/git` 注入 PATH（越界、影响所有 git 调用）。
- boundary_non_goals: 不改 `.githooks/post-checkout` 一个字节；不改外部项目合法早退；不改 `pr-create-guarded` 正常无 raw key 路径；不让 file-size 历史遗留阻断未来提交；不接线 `.githooks/bin/git`；不夹带 R11/#4149、#4151。
- residual_risk: ①`.githooks/bin/git` 仍未接入 PATH，`--no-verify` 在技术上仍可绕过客户端 hook（文档不再宣称已拦截，需另开 issue 处理基础设施接线）。②`check-file-size` 全量运行约 58s（治理文档扫描开销），但 pre-commit 只用增量模式（毫秒级）。③4 个预存红测试归 #4151 / R1 记录。
- verification: AT-001 基线 RED 26 失败 / 2 既有能力 PASS → GREEN 28/28；隔离仓库真实 `git commit` 验证缺真身被拒、`+x` 丢失仍执行；真实工位 `git commit` 冒烟 exit 0 / 1s 确认不自锁；14 个回归以未修改 develop HEAD 基线对比 0 新增失败；check-epics-map 对齐。
- self_bootstrap_findings: 本轮未发现「现有 open issue 未覆盖」的新缺陷；4 个预存红测试与 deprecated merge-guarded ENOENT 已被 #4151 / R1 覆盖，未重复立项。
