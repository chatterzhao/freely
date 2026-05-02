# Brainstorm: acp-optional-adapter-boundary-governance

## Key Decisions

1. ACP 在 Freely 中只作为 optional adapter layer 研究与 materialize，不作为治理替代品。
2. `direct` 保持 first-class；ACP 不是未来唯一接入方式。
3. 每个工具独立声明 adapter policy，比“全局切 ACP”更符合 Freely 当前现实。
4. real-tool dual-path validation 留给 follow-on implementation owner，不回塞 candidate。

## Main Tension

Freely 的痛点确实开始落在外部 agent 接入异构上，但解决方案如果直接变成“让 ACP 接管一切”，就会破坏 Freely 已经成熟的 continuity、recovery 与 dogfooding 治理面。边界必须同时满足：

- 新增工具更容易接入
- 现有成熟直连路径不被迫重写
- experimental tool reality 继续被诚实标注

## Chosen Boundary

- ACP 只收 communication plane
- Freely 保留 control plane
- `adapter axis` 先于 first-tool prototype
- candidate-level research 到此为止，后续进入 issue-guided implementation

## Expected Landing

完成后，后续实现不再需要重新争论这些问题：

1. ACP 到底是不是治理平面
2. 直连是不是临时方案
3. 真实双路径测试属于 candidate 还是 issue
4. `cc` 这类实验性实现能否直接当 promised surface

后续 owner 只需要继续回答：

1. 先怎样抽 `adapter axis`
2. 第一刀选哪个 current-repo tool
3. 怎样跑真实工具 dual-path acceptance
