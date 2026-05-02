# Brainstorm: runtime-adapter-axis-and-per-tool-adapter-selection

## Key Decisions

1. 这条 owner 只做 adapter axis extraction，不做 ACP bridge。
2. `direct` 继续是 default path，不对 current tools 做强制迁移。
3. unsupported adapter 必须 fail fast，不能隐式 fallback。

## Main Tension

如果只在文档里说“以后可以 direct/acp 双轨”，但 runtime 仍只有 `AI_TOOL + tool-specific launcher`，后续实现就会继续在错误抽象上叠 patch。真正的第一刀必须把 selection axis 先抽出来，同时又不能打碎当前 continuity truth。

## Chosen Boundary

- config 先引入 `AI_TOOL_ADAPTER`
- tool metadata 冻结 default/supported adapters
- dispatch 先 adapter 后 tool
- direct path 先保守落地

## Expected Landing

完成后，follow-on ACP prototype 不再需要先争论：

1. adapter 该放在哪个 truth surface
2. 该不该静默 fallback 到 direct
3. status / continuity 应该看哪套 adapter truth
