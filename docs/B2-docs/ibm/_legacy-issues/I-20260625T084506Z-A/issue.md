<!-- I-* frontmatter 使用 bullet 格式（- key: value），不用 YAML --- 包裹。
     canonical reader (cgrab) 解析 bullet 和 YAML 均可，但 bullet 是推荐格式。 -->
- issue_id: I-20260625T084506Z-A
- kind: fix
- phase_state: completed
- milestone: M-20260625T084506Z-A
- source_candidate: docs/B1-docs/raw-20260625T084506Z/candidates.md#C-20260625T084506Z-A
- verification_artifact_dir: docs/epics/b2-ibm-anti-cheating/code-reviews
- canonical_issue_path: docs/B2-docs/ibm/_legacy-issues/I-20260625T084506Z-A/issue.md
- source_raw: raw-20260625T084506Z
- pre_tests_path: docs/epics/b2-ibm-anti-cheating/verification/pre-tests.md
- title: B2_IBM skill 反糊弄铁律 + gate E2E/集成测试层级检查

# I-20260625T084506Z-A: B2_IBM skill 反糊弄铁律 + gate E2E/集成测试层级检查

- source_candidate: docs/B1-docs/raw-20260625T084506Z/candidates.md#C-20260625T084506Z-A
- verification_artifact_dir: docs/epics/b2-ibm-anti-cheating/code-reviews
- pre_tests_path: docs/epics/b2-ibm-anti-cheating/verification/pre-tests.md

## 实现

### 改动 1: B2_IBM SKILL.md
- pre-tests.md 模板前加入「反糊弄铁律」醒目警告
- 明确：每条 acceptance item 必须是真实测试用例
- 明确：端到端测试和集成测试是 AI 编程防失败最重要保证
- 明确：糊弄是导致项目失败的严重失职行为
- 改动文件: docs/system/workspace/skills/freely-doc-B2_IBM-execution/SKILL.md

### 改动 2: pretests-retirement-gate
- 新增端到端/集成测试层级充分性硬拦截
- 扫描 acceptance items 的 testing_layer 字段
- 检查 ## End-to-End 和 ## Integration 层级章节
- 无真实测试 + not_applicable_reason 为占位符 → 硬拦截
- 报错强制指向 B2_IBM 和 test-execution skill
- 改动文件: docs/system/workspace/scripts/quality/pretests-retirement-gate
