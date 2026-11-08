# Brainstorms: raw-20261104T084406Z

## 问题

`freely feedback --severity P0|P1|P2` 只做参数校验，之后优先级在四个环节全部丢失：

1. `runtime/freely:25184-25187` 校验取值合法，随后丢弃；
2. `runtime/freely:25240-25259` 用 `new_raw_metadata()` 构造 frontmatter，不传 severity；
3. `platform-adapter.py:818 / 1534` 的 `create_issue(local_id, title, body)` 与 CLI 都只接受 3 参，**根本没有 labels 通道**；GitHub/Gitee handler 的 `create_issue(title, body)` 也不带 label；
4. `bin/issue-sync:_labels()` 只输出 `kind/*` + `phase/*`，`cmd_scan()` 按 `find` 顺序输出，无优先级排序。

结果：P0 与 P2 在平台与本地完全同权，只能靠外部 goal 文件人工维护分诊顺序。

## 证据（本机实测）

- RED 基线快照（`git archive develop -- bin docs` + 最终版 AT-001）：`SUMMARY: 3 ok, 14 failed`。`--severity P0` 生成的 body frontmatter 无 severity；`create-issue` argv 的第 5 项 labels 为空；`_labels` 输出仅 `kind/raw,phase/proposed`；`create_issue()` 传第 4 参直接 `TypeError`。
- 契约现状：`RAW_METADATA_FIELDS` 是严格 21 字段元组，`validate()` 用 `tuple(keys) != RAW_METADATA_FIELDS` 拒绝任何额外字段；develop 上 59 份 strict 文档 + 824 份历史 raw 都不含 severity。

## 证伪（未被现有 open issue 覆盖）

- #4149（R11 已合并）修的是写通道失败必报与部分成功退出码，未涉及 severity 字段或 label。
- #4154（契约常量与 raw key 多副本收口）针对常量与副本，不含优先级语义。
- #4166（双平台入口收口）是入口层重构，不含「优先级字段落盘 + 标签 + 排序」这条数据链。
- #4151（测试证据链）是证据可验证性，与本条无关。

## 关键设计

1. **severity 是可选第 22 字段**，不是必填：`RAW_METADATA_FIELDS_WITH_SEVERITY = RAW_METADATA_FIELDS + ("severity",)`；`validate()` 接受两种合法形状并在字段存在时校验 P0/P1/P2。绝不批量重写 824 份历史文档（R2 先例）。
2. **存量回填放在 read view**：`normalize()` 与 `issue-sync._labels()` 对无字段/非法值统一解析为 `P2`，零文件改动。
3. **labels 通道向后兼容**：`platform-adapter.create_issue(..., labels="")` 仅在 labels 非空时把第 3 参传给 handler；旧调用与自定义 handler 仍走 2 参路径。GitHub 用 `gh issue create --label`，Gitee 用 `gitee-issue.py create --labels`。
4. **scan 稳定排序**：收集行到数组、加 P0/P1/P2 rank 前缀、`sort -s` 后剥前缀，同级保持原发现顺序；输出行带 `sev=Pn` 供核对。

## 被否决的替代方案

- 把 severity 加进 `RAW_METADATA_FIELDS` 成必填 22 字段：会让 `validate()` 拒绝全部 59 份 strict 文档与 `new_raw_metadata()` 自身输出，必须批量改写 824 份文件 —— 明确退化。
- 批量回填历史文件：噪音大、无业务收益，与只读回填语义重复。
- 只加平台 label、不写 frontmatter：本地仍丢，且「平台有、本地无」会破坏副本一致性。
- 把 severity 塞进 body 文本：不能按 label 过滤，验收标准 2 无法满足。
