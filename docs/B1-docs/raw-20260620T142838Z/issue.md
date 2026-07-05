---
local_id: raw-20260620T142847Z38Z
kind: raw
phase_state: absorbed
absorbed_into: I-20260620T142838Z-A
platform_ids:
  github:
    issue_id: '3173'
    url: https://github.com/chatterzhao/freely/issues/3173
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-06-20T14:28:54Z'
updated_at: '2026-06-20T14:28:54Z'
intake_id: ''
author: platform
channel: github
session_refs: []
---

## 问题

`governance-merge-gate` 的 `parse_issue_file()` 中，`grab()` 支持 bullet 和 YAML 双格式，但 `cgrab()`（canonical reader，L486）只支持 bullet 格式。

当 I-* issue 文件使用了 YAML frontmatter（`---` 包裹），canonical reader 把所有字段（phase_state, milestone, source_candidate）置 None → issue "cannot be resolved" → IBM Completeness 失败。

## 修复

### governance-merge-gate L486-488

`cgrab` 加 YAML fallback，与 `grab` 一致：

```python
def cgrab(name: str) -> Optional[str]:
    # bullet 格式: "- key: value"
    m = re.search(rf"^\s*-\s*{re.escape(name)}:\s*(.+?)\s*$", canonical_text, re.MULTILINE)
    if m: return normalize_scalar(m.group(1))
    # YAML 格式: "key: value" at line start  <-- 新增
    m = re.search(rf"^{re.escape(name)}:\s*(.+?)\s*$", canonical_text, re.MULTILINE)
    return normalize_scalar(m.group(1)) if m else None
```

### skill 文档更新

`docs/system/workspace/skills/freely-doc-B2_IBM-execution/SKILL.md`：
- 常见错误表加 "phase_state 等字段被清空" → "I-* issue 文件 frontmatter 格式：bullet（`- key: value`）和 YAML（`key: value`）均可，推荐 bullet"
- I-* 示例注释标注格式要求

## 影响文件
- `docs/system/workspace/scripts/quality/governance-merge-gate` — cgrab 加 YAML fallback
- `docs/system/workspace/skills/freely-doc-B2_IBM-execution/SKILL.md` — 常见错误表 + 格式说明
