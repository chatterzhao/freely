# IBM Framework documentation - verification

- issue_id: `I-20260426-0000-A`

## Implementation Decision Note
- decision: `Formalize IBM Framework with B1_IBM/B2_IBM naming. B1_IBM: Input→Brainstorm→Milestone. B2_IBM: Input→Brainstorm→Map. Brainstorm is the core engine, IBM is the I-B-M skeleton.`
- why_this: `Terminology was inconsistent across AGENTS.md, PROJECT_INTENT.md, CONSTITUTION.md, three-loop doc, LAWS.md, skills, and agents. IBM Framework now provides one canonical name for the two-phase governance structure.`
- alternatives_considered: `1) Keep old names (预研头脑风暴/IBM 头脑风暴): rejected, inconsistent and doesn't convey I-B-M structure. 2) B1/B2 without _IBM suffix: rejected, loses the I-B-M meaning. 3) B1_IBM/B2_IBM: chosen, preserves both phase label and I-B-M structure.`
- boundary_non_goals: `No directory restructure. No phase_state changes in runtime code. No skill renaming. No historical document updates.`
- residual_risk: `Phase states (todo_ibm etc.) and skill name (doc-ibm-execution) remain as legacy; follow-on issue needed for runtime sync.`
