# Brainstorm: ibm-pretests-executable-acceptance-quality-governance

## Key Decisions

1. 这不是 `I-20260322-0135` 的 reopen，而是它的 enforcement follow-on。
2. 本轮只改 IBM 真源与 checklist，不把 verification review 模板一起拖进来。
3. 允许不同 issue 用不同形式的证据组合，但不允许缺少 acceptance contract：
   - focused regression
   - integration scenario
   - application-native real-environment scenario
   - end-to-end dogfood scenario

## Main Tension

不能把“真实环境测试必做”误写成“每条 issue 都必须新写自动化脚本”。Freely 的很多验收面本来就需要通过真实 runtime、`freely chat`、manager patrol、worker handoff、status surfaces 来观察。问题不在测试类型必须单一，而在 `pre-tests.md` 必须先把这些面写出来，而不是 merge 后再临场补推理。

## Chosen Boundary

- 这轮收紧的是 IBM 质量门槛
- 不要求重写历史 issue
- 不要求同步结构化所有 verification review 文件
- 但要求新的 `pre-tests.md` 最小上能恢复：
  - environment
  - evidence
  - failure signal
  - replay / failure-handling expectation

## Expected Landing

完成后，后续治理型 issue 不能再只用“读某文档应能看出语义”作为主验收面；至少要解释：

1. pre-merge 应跑什么 focused regression / smoke
2. merge 后在哪个 protected environment 做 integration / real-environment / dogfood acceptance
3. 如果某类不适用，为什么不适用，替代证据是什么
