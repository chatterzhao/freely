# code-review: raw-20260624T104236Z

- raw_issue_key: raw-20260624T104236Z
- github_issue: #3428
- branch: fix/raw-20260624T104236Z-fix-govern-first-skill-pointer

## Implementation Decision Note

**Problem**: Users (both human and AI) could see the phrases "Fix first, govern later" and "Govern first, code later" without knowing where to find the complete workflow steps. This led to misinterpretation and skipping of proper process.

**Solution**: Add inline pointers after every occurrence of these phrases in both `freely-fix-execution` and `freely-feat-execution` skill files, directing readers to the full skill documentation.

**Changes**:

1. `docs/system/workspace/skills/freely-fix-execution/SKILL.md`:
   - Frontmatter `description`: Added `（完整工作流见本 skill 文档）` after "Fix first, govern later"
   - §核心原则 blockquote: Added `完整工作流见本 skill 文档（§工作流、§场景 A、§场景 B）` as a new blockquote line after the "Fix first, govern later" line

2. `docs/system/workspace/skills/freely-feat-execution/SKILL.md`:
   - §与 freely-fix-execution 的分工 table: Added `（完整工作流见 skill:freely-fix-execution 文档）` and `（完整工作流见 skill:freely-feat-execution 文档）` to the respective table cells

**Impact**: Zero runtime impact. Only documentation/skill description changes. Users who see these phrases in skill listings or documentation will now know exactly where to find the complete workflow.

## Files changed

- `docs/system/workspace/skills/freely-fix-execution/SKILL.md` (+2 lines)
- `docs/system/workspace/skills/freely-feat-execution/SKILL.md` (+1 line)
- `~/.claude/skills/freely-fix-execution/SKILL.md` (deployed via deploy-skills)
- `~/.claude/skills/freely-feat-execution/SKILL.md` (deployed via deploy-skills)
