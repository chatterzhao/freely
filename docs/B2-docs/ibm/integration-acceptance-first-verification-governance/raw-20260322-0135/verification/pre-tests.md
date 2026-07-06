# Pre-tests: integration-acceptance-first-verification-governance

## Acceptance Structure

### Pre-merge acceptance

1. `doc-ibm-execution` 与 IBM references 明确：
   - `pre-tests.md` 是 issue-level acceptance 控制面
   - `pre-tests.md` 默认以 integration / acceptance 为主
2. `three-loop-capability-lifecycle` 明确：
   - verification 默认先看 integration / acceptance evidence
   - code review 是二级验证面
3. `LAWS.md` 明确：
   - develop 合并 gate 以 integration / acceptance evidence 为主

### Post-merge acceptance

1. 后续新的 issue 若需要 merge 后验收，必须能在自己的 `pre-tests.md` 里显式区分：
   - `pre-merge`
   - `post-merge`

### Non-goals

1. 不要求本 issue 同时改造所有历史 verification review 文件
2. 不要求在本 issue 中统一所有测试命名规范
