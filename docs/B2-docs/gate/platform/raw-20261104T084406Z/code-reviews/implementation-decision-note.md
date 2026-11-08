# Implementation Decision Note
- issue_id: I-20261104T084406Z-A
- decision: severity 作为可选第 22 字段落 frontmatter、以 `severity/Pn` 标签贯穿双平台建单、scan 按 P0→P2 稳定排序；存量在读视图回填 P2，零历史文件改写
- why_this: `--severity` 校验后在 frontmatter、平台 body/label、scan 三处全部丢失，且 `platform-adapter.create_issue()` 根本没有 labels 通道，导致优先级无法分诊，只能靠外部 goal 文件人工维护。
- alternatives_considered: ①把 severity 加进 `RAW_METADATA_FIELDS` 成必填 22 字段（会拒绝 59 份 strict 文档并迫使 824 份历史文件重写，明确退化）；②批量回填历史文件（噪音大、零收益）；③只加平台 label 不写 frontmatter（本地仍丢且破坏副本一致性）；④把 severity 塞进 body 文本（不能按 label 过滤）。
- boundary_non_goals: 不改关闭路径四段式与 0/3/1 退出码；不改副本一致性、test-gate、promote 链路；不新建 story（复用 gate/platform，epics-map 不变）；不改任何平台已存在 issue。
- residual_risk: ①GitHub 侧 `gh issue create --label` 要求标签已存在或 gh 自动创建，若仓库禁用自动建标签则该次建单会带 error，需要在真实创建时观察；Gitee `--labels` 同理。②`scan` 输出新增 `sev=Pn` 字段，若有外部脚本按固定列数解析需复核（仓库内无此类调用）。③`severity` 只在新建时写入；历史 raw 的平台副本不会补标签，读视图与本地标签统一按 P2 展示。④自定义 3 参 handler 未覆盖，只守护了 2 参旧路径与内置双平台 3 参路径。
- verification: AT-001 develop 基线快照 RED `3 ok / 14 failed` → 工位 GREEN `30 ok / 0 failed`；14 个相关回归 worktree/baseline 退出码全 MATCH（1 项预存红两边一致）。
- self_bootstrap_findings: 本轮未发现「现有 open issue 未覆盖」的新缺陷；#4149/#4154/#4166/#4151 均已证伪覆盖不到本条数据链。

## Implementation Decision Note
- decision: 可选第 22 字段 + 读视图回填 + 双平台 severity 标签 + scan 稳定排序
- why_this: severity 校验后四处全丢，adapter 无 labels 通道
- alternatives_considered: 必填字段 / 批量回填 / 只加 label / 塞进 body
- boundary_non_goals: 关闭路径、副本一致性、test-gate、promote、epics-map 均不动
- residual_risk: 平台标签需已存在（真机待观察）；scan 输出新增 sev 字段；历史副本不补标签；3 参自定义 handler 未覆盖
