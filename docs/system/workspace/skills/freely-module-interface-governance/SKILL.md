---
name: freely-module-interface-governance
description: >-
  应用可插拔模块和接口版本治理，支持并行演进。覆盖模块替换、
  版本化契约和模块间迁移路径。

  Use when: 引入模块替换、版本化接口或模块间迁移。
  触发词："模块治理"、"接口版本"、"migration path"、"替换模块"。
---

# skill:freely-module-interface-governance

## 工作流

1. 定义模块边界和当前契约版本。
2. 如涉及第三方 API，将提供方契约视为外部事实源，围绕其设计本地适配器。
3. 对于破坏性变更，创建版本化契约和迁移路径。
4. 保持到稳定实现的回滚路径。
5. 用测试验证契约兼容性。
6. 需要场景对照时读取 [examples.md](references/examples.md)。
7. 记录活跃版本和切换策略。

## 完成
- 模块演进已版本化、可测试、可逆，并在使用时对齐第三方 API 契约。
