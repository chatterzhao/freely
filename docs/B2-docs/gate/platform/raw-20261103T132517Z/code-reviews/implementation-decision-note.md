# Implementation Decision Note
- issue_id: I-20261103T132517Z-A
- issue_path: docs/B2-docs/gate/platform/raw-20261103T132517Z/issues/I-20261103T132517Z-A.md
- decision: 把 frontmatter 解析与写入的所有权收到 `raw_metadata_contract`，删除 scan 的手写解析与 issue-sync 的内联解析；解析失败产显式 `metadata_validation_error`；repair 覆盖 B1 + B2 四类损坏；**历史 bullet 格式保留为受支持格式**
- why_this: 三套解析器里两套 `except: pass` / `2>/dev/null || true`，坏文档静默变空 metadata，该 issue 从生命周期消失但仍被计为完成，Manager 只能靠「AI 反复做无用功」间接察觉。规范实现（严格校验 + 原子写）早就在仓库里，只是运行时路径不用它。
- alternatives_considered: ①只修 23 份数据不收口所有权（修完仍复发）；②给 scan 再写一套严格解析（变成第四个所有者）；③把 184 份历史 bullet 文档全量改写成 YAML（改动面远超本 issue，历史 diff 不可读）；④解析失败直接抛异常中断 scan（一条坏文档挂掉整个扫描，比静默更糟）；⑤`=======` 单独出现即判冲突（误伤 Markdown setext 标题）。
- boundary_non_goals: 不改 raw 21/22 字段契约与 severity 语义；不改 `bin/issue-sync` 对外命令语义与退出码约定；不做 B2 全量格式统一；不改平台侧 issue 内容；不动任何门禁检查。
- residual_risk: ①`bin/issue-sync` 新增对 `lifecycle/frontmatter_contract_cli.py` 的硬依赖——真实打包走 `docs/system/workspace/scripts/` 整目录已覆盖，但「只复制 `bin/issue-sync` 单文件」的用法会静默失效（`_fm_*` 仍是 `2>/dev/null || true`）；本轮只把已知 5 个夹具补齐，未把该依赖变成显式启动检查，后续可考虑 CLI 缺失时 fail loud。②`parse_frontmatter` 在 YAML 有效时不读 bullet，因此正文里 `- key: value` 形式的说明列表不会被识别为 metadata——这是刻意复刻收口前语义，但意味着「正文补充元数据」这种写法永远不受支持。③repair 的字段白名单 `_KNOWN_FIELDS` 是人工维护集合，新增契约字段时若忘记加入，粘连修复会漏。④全量对比口径是「字段级一致」，不是「字节级一致」；repair 会用 `yaml.safe_dump` 重排格式，23 份文档的 diff 含格式变化。
- verification: AT-001 develop 基线快照 RED `7 ok / 14 failed` → 工位 GREEN `21 ok / 0 failed`；18 项相关回归 worktree/baseline 退出码对比（明细见 AT-001-REGRESSION-BASELINE.log）；全量 1082 份 B1+B2 文档解析差异 25 份（23 修复 + 2 新增）、其余 1057 份字段级一致、`metadata_validation_error` 计数 0；真机 repair 幂等（第二次 dry-run damaged=0）；`bin/test-all --ci` 退出 0。
- self_bootstrap_findings: ①初版把 bullet fallback 一起删掉，全量实测立刻暴露 184 份历史文档被误判损坏 + 186 处 `phase_state` 丢失——已改为「无 YAML 时用 bullet，YAML 有效时不补 bullet」；②冲突标记用 `=======` 单独判定会误伤 setext 分隔线，改为成对匹配；③`_fm_*` 改成外部 CLI 后，5 个只复制 `bin/issue-sync` 的测试夹具静默失效，`platform_state`/`promoted_children`/`severity` 三类写入消失——已补齐夹具并加静态守卫。这三条都是「修 A 坏 B」的典型，全部由全量对比而非单点测试发现。

## Implementation Decision Note
- decision: 单一所有者 + 失败可见 + 幂等修复 + 历史格式保留
- why_this: 静默空 metadata 让 issue 从生命周期消失且无告警
- alternatives_considered: 只修数据 / 第四套解析 / 全量改写 / 抛异常中断 / 宽松冲突判定
- boundary_non_goals: 字段契约、命令语义、B2 格式统一、平台内容、门禁检查均不动
- residual_risk: 单文件复制场景静默失效、正文 bullet 不受支持、白名单需人工维护、repair 含格式重排
