# 研究：EvoMap SDK 与 MCP 接入深度分析

## Context

经过深入调研，EvoMap 生态提供多个接入方式：

| 接入方式 | 定位 | 适用场景 |
|----------|------|----------|
| **Evolver CLI** | 进化引擎 | 本地自我进化 |
| **@evomap/sdk** | Node.js SDK | 编程式接入 |
| **A2A 协议** | HTTP API | 任何语言/平台 |
| **MCP** | 工具协议 | 与 Claude 等 Agent 集成 |

## 一、@evomap/sdk 分析

### 1.1 核心 API

```javascript
const { Agent } = require('@evomap/sdk');

const agent = new Agent({
  name: 'my-evolver',
  evolveStrategy: 'balanced'  // balanced | innovate | harden | repair-only
});

// 监听进化信号
agent.on('signal', (sig) => {
  console.log('Evolution signal:', sig.type);
});

// 运行
agent.run();
```

### 1.2 与 Freely 的整合点

```javascript
// Freely 可以这样使用
const { Agent } = require('@evomap/sdk');

class FreelyEvolver {
  constructor(config) {
    this.agent = new Agent({
      name: 'freely-agent',
      evolveStrategy: this.mapStrategy(config.issueType)
    });
  }

  mapStrategy(issueType) {
    const mapping = {
      'bug': 'repair-only',
      'optimization': 'harden',
      'feature': 'innovate',
      'default': 'balanced'
    };
    return mapping[issueType] || mapping.default;
  }
}
```

## 二、A2A 协议端点

### 2.1 核心端点

| 端点 | 功能 | 用途 |
|------|------|------|
| `POST /a2a/hello` | 节点握手 | 注册 Agent |
| `POST /a2a/publish` | 发布资产 | 上传 Gene/Capsule |
| `POST /a2a/fetch` | 获取资产 | 下载他人资产 |
| `POST /a2a/report` | 反馈效果 | 使用报告 |

### 2.2 调用示例

```bash
# 注册 Agent
curl -X POST https://evomap.ai/a2a/hello \
  -H "Content-Type: application/json" \
  -d '{
    "protocol": "gep-a2a",
    "version": "1.0.0",
    "type": "hello",
    "sender_id": "freely-agent-001",
    "payload": {
      "name": "Freely Agent",
      "capabilities": ["issue_management", "code_review", "testing"]
    }
  }'

# 获取资产
curl -X POST https://evomap.ai/a2a/fetch \
  -H "Content-Type: application/json" \
  -d '{
    "protocol": "gep-a2a",
    "version": "1.0.0",
    "type": "fetch",
    "sender_id": "freely-agent-001",
    "payload": {
      "query": "disk_check",
      "min_gdi": 0.8,
      "environment_match": "relaxed"
    }
  }'
```

## 三、MCP 与 GEP 的关系

### 3.1 三层协议栈

```
┌─────────────────────────────────────────┐
│           GEP (进化层)                    │
│   Why + How + What（验证过的经验）         │
│   - Gene：策略模板                        │
│   - Capsule：验证修复                     │
│   - GDI：质量评分                         │
├─────────────────────────────────────────┤
│           Skill (操作层)                  │
│   How + What（怎么做）                    │
│   - 步骤化操作指令                         │
│   - 专家经验编码                          │
├─────────────────────────────────────────┤
│           MCP (接口层)                    │
│   What（有什么工具）                       │
│   - 工具发现与调用                         │
│   - 标准化接口                            │
└─────────────────────────────────────────┘
```

### 3.2 类比理解

| 协议 | 生物类比 | 功能 |
|------|----------|------|
| MCP | 神经系统 | 感知外部环境，调用工具 |
| Skill | 肌肉记忆 | 执行具体动作 |
| GEP | 免疫系统 | 学习、适应、传承 |

## 四、Freely 接入方案

### 4.1 方案对比

| 方案 | 实现复杂度 | 功能完整度 | 推荐度 |
|------|-----------|-----------|--------|
| **A: 纯 CLI 调用 Evolver** | 低 | 中 | ⭐⭐⭐ |
| **B: 使用 @evomap/sdk** | 中 | 高 | ⭐⭐⭐⭐ |
| **C: 直接 A2A 协议** | 高 | 高 | ⭐⭐ |
| **D: 混合方案** | 中 | 高 | ⭐⭐⭐⭐⭐ |

### 4.2 推荐方案：混合架构

```
Freely
    │
    ├── CLI 调用 Evolver（本地进化）
    │   └── node index.js --strategy=xxx
    │
    ├── @evomap/sdk（编程接口）
    │   ├── Agent 类
    │   ├── 信号监听
    │   └── 资产管理
    │
    └── A2A 协议（网络共享）
        ├── 发布高质量 Capsule
        └── 获取他人验证过的方案
```

### 4.3 接入步骤

#### Step 1: 安装依赖

```bash
npm install @evomap/sdk
# 或
git clone https://github.com/EvoMap/evolver
```

#### Step 2: Freely 集成层

```javascript
// src/evolver/adapter.js
const { Agent } = require('@evomap/sdk');
const { execSync } = require('child_process');

class FreelyEvolverAdapter {
  constructor(config) {
    this.config = config;
    this.agent = null;
  }

  // 方式 1: SDK 接入
  async initSDK() {
    this.agent = new Agent({
      name: this.config.agentName,
      evolveStrategy: this.config.strategy
    });

    this.agent.on('signal', (sig) => {
      this.handleSignal(sig);
    });
  }

  // 方式 2: CLI 调用
  async evolveCLI(strategy) {
    const output = execSync(
      `node ${this.config.evolverPath}/index.js --strategy=${strategy}`,
      { encoding: 'utf-8' }
    );
    return this.parseOutput(output);
  }

  // 方式 3: A2A 协议
  async fetchCapsule(query) {
    const response = await fetch('https://evomap.ai/a2a/fetch', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        protocol: 'gep-a2a',
        version: '1.0.0',
        type: 'fetch',
        sender_id: this.config.senderId,
        payload: query
      })
    });
    return response.json();
  }
}
```

#### Step 3: 与质量门禁整合

```javascript
// src/evolver/gate.js
class EvolutionGate {
  async validate(capsule) {
    // 宪法检查
    if (!this.checkConstitution(capsule)) {
      return { passed: false, reason: '不符合宪法约束' };
    }

    // 验收标准检查
    if (!capsule.acceptanceCriteria) {
      return { passed: false, reason: '缺少验收标准' };
    }

    // GDI 评分检查
    if (capsule.gdi < 0.7) {
      return { passed: false, reason: 'GDI 评分过低' };
    }

    return { passed: true };
  }
}
```

## 五、价值评估

### 5.1 Freely 获得

| 能力 | 来源 | 价值 |
|------|------|------|
| 自我进化 | Evolver 引擎 | 自动修复、优化 |
| 能力继承 | A2A 网络 | 全球共享方案 |
| 质量评分 | GDI 系统 | 量化验证 |
| 跨 Agent 协作 | 生态网络 | 群体智能 |

### 5.2 实施优先级

| 优先级 | 任务 | 工作量 |
|--------|------|--------|
| P0 | CLI 调用 Evolver | 1-2 天 |
| P1 | A2A 注册与 Fetch | 2-3 天 |
| P2 | @evomap/sdk 集成 | 3-5 天 |
| P3 | Publish Capsule | 2-3 天 |

## 六、结论

**推荐接入路径**：

```
Phase 1: CLI 调用 Evolver（验证可行性）
    ↓
Phase 2: A2A Fetch（获取他人方案）
    ↓
Phase 3: @evomap/sdk 深度集成（完整能力）
    ↓
Phase 4: A2A Publish（贡献方案）
```

**核心价值**：Freely 从"任务执行器"升级为"进化系统"，同时保持 CLI 编排的简洁架构。