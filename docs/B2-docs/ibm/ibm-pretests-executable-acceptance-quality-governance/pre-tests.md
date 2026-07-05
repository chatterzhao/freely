# Pre-tests: ibm-pretests-executable-acceptance-quality-governance

## Acceptance Structure

### Pre-merge focused regression / smoke

1. `doc-ibm-execution` 明确：
   - `pre-tests.md` 默认是 executable acceptance contract
   - wording review 只能是补充面，不是主验收面
2. `prd-quality-bar` 明确：
   - `Eval Plan` 必须先写 environment / evidence / failure signal / replay expectation
   - `pre-tests.md` 默认不能只由阅读检查构成
3. `ibm-completion-gate` 与 `issue-materialization-checklist` 明确：
   - Freely 自治能力默认要回答 integration / application-native real-environment / end-to-end dogfood 三类 post-merge acceptance
   - 若不适用，必须写出不适用理由与替代证据

### Post-merge integration acceptance

1. 在 `develop` 上继续 materialize 新 issue 时，后续 `pre-tests.md` 必须更自然地写出：
   - target environment
   - evidence
   - failure signal
   - failure handling / replay expectation
2. 对只写 wording review 的弱 `pre-tests.md`，应能直接从更新后的 IBM 真源看出它不达标。

### Post-merge application-native real-environment acceptance

1. 对 Freely 自治能力类 issue，`pre-tests.md` 必须能要求至少一条真实 runtime 观察场景，例如：
   - `freely start`
   - `freely chat`
   - manager patrol / worker delegation
   - status / live-status / fleet-status 证据面
2. 若某条 issue 不需要这类场景，`pre-tests.md` 必须显式说明不适用理由，而不是默默省略。

### Post-merge end-to-end dogfood acceptance

1. 对会影响 Freely 自举流程的 issue，`pre-tests.md` 必须能要求至少一条 dogfood continuation / interruption / replay 场景，证明 acceptance contract 能在真实工作流里被消费。
2. 若该类场景不适用，必须写明替代证据面。

### Non-goals

1. 不在本 issue 中统一历史 code review 文件格式。
2. 不要求本 issue 同时引入新的测试 runner 或自动化 harness。
