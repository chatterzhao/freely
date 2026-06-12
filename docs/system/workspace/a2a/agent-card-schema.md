# Freely Agent Card JSON Schema

> 本文档定义 Freely Worker Agent Card 的 JSON Schema，包含 A2A 标准字段和 Freely 扩展。

## 完整 Schema

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "description": "Freely Worker Agent Card - A2A compatible with Freely extensions",
  "properties": {
    "$schema": {
      "type": "string",
      "description": "JSON Schema 引用"
    },
    "name": {
      "type": "string",
      "description": "Agent 名称",
      "examples": ["Freely Worker", "Freely Manager"]
    },
    "description": {
      "type": "string",
      "description": "Agent 功能描述",
      "examples": ["Freely Worker Agent with worktree isolation"]
    },
    "url": {
      "type": "string",
      "format": "uri",
      "description": "Agent 服务 URL"
    },
    "version": {
      "type": "string",
      "pattern": "^\\d+\\.\\d+\\.\\d+$",
      "description": "Agent 版本"
    },
    "capabilities": {
      "type": "object",
      "properties": {
        "streaming": {
          "type": "boolean",
          "description": "是否支持 SSE 流式推送"
        },
        "pushNotifications": {
          "type": "boolean",
          "description": "是否支持推送通知"
        },
        "stateTransitions": {
          "type": "boolean",
          "description": "是否支持状态转换推送"
        }
      }
    },
    "skills": {
      "type": "array",
      "description": "Agent 支持的 skills 列表",
      "items": {
        "type": "object",
        "properties": {
          "id": {
            "type": "string",
            "description": "Skill ID",
            "examples": ["freely-fix-execution", "freely-feat-execution"]
          },
          "name": {
            "type": "string",
            "description": "Skill 名称"
          },
          "description": {
            "type": "string",
            "description": "Skill 描述"
          },
          "inputModes": {
            "type": "array",
            "items": { "type": "string" },
            "description": "支持输入模式",
            "examples": [["text", "json"]]
          },
          "outputModes": {
            "type": "array",
            "items": { "type": "string" },
            "description": "支持输出模式"
          }
        },
        "required": ["id", "name"]
      }
    },
    "authentication": {
      "type": "object",
      "description": "认证配置",
      "properties": {
        "schemes": {
          "type": "array",
          "items": { "type": "string" },
          "description": "支持的认证方案"
        }
      }
    },
    "defaultErrorHandlingMode": {
      "type": "string",
      "enum": ["text", "developer", "agentic"],
      "description": "默认错误处理模式"
    },
    "freely": {
      "type": "object",
      "description": "Freely 扩展字段",
      "properties": {
        "agentType": {
          "type": "string",
          "enum": ["manager", "worker"],
          "description": "Agent 类型"
        },
        "worktreeIsolation": {
          "type": "boolean",
          "description": "是否支持 worktree 隔离"
        },
        "worktreeRoot": {
          "type": "string",
          "description": "Worktree 根目录路径"
        },
        "supportedExitKinds": {
          "type": "array",
          "items": { "type": "string" },
          "description": "支持的所有 exit_kind 类型"
        },
        "handoffJsonSchema": {
          "type": "string",
          "format": "uri",
          "description": "Handoff JSON Schema URL"
        },
        "supportedSkills": {
          "type": "array",
          "items": { "type": "string" },
          "description": "Freely skill 列表"
        },
        "transport": {
          "type": "string",
          "enum": ["unix-domain-socket", "http"],
          "description": "传输层类型"
        },
        "socketPath": {
          "type": "string",
          "description": "Unix Domain Socket 路径"
        },
        "runtime": {
          "type": "object",
          "description": "Freely runtime 配置",
          "properties": {
            "version": {
              "type": "string",
              "description": "Freely runtime 版本"
            },
            "tool": {
              "type": "string",
              "description": "AI CLI 工具类型"
            },
            "model": {
              "type": "string",
              "description": "AI 模型"
            },
            "mode": {
              "type": "string",
              "enum": ["auto", "step"],
              "description": "执行模式"
            }
          }
        },
        "projectRoot": {
          "type": "string",
          "description": "托管项目根目录"
        },
        "branch": {
          "type": "string",
          "description": "当前分支"
        }
      },
      "required": ["agentType"]
    }
  },
  "required": ["name", "description", "url", "version", "capabilities", "skills"]
}
```

## 示例

### Manager Agent Card

```json
{
  "name": "Freely Manager",
  "description": "Freely Manager Agent - orchestrates workers and manages task lifecycle",
  "url": "http://localhost:7891",
  "version": "1.0.0",
  "capabilities": {
    "streaming": true,
    "pushNotifications": true,
    "stateTransitions": true
  },
  "skills": [],
  "defaultErrorHandlingMode": "agentic",
  "freely": {
    "agentType": "manager",
    "worktreeIsolation": true,
    "supportedExitKinds": [],
    "supportedSkills": [
      "freely-fix-execution",
      "freely-feat-execution",
      "freely-doc-B1_IBM-execution",
      "freely-doc-B2_IBM-execution"
    ],
    "transport": "unix-domain-socket"
  }
}
```

### Worker Agent Card

```json
{
  "name": "Freely Worker",
  "description": "Freely Worker Agent with worktree isolation for skill-based execution",
  "url": "http://localhost:7890",
  "version": "1.0.0",
  "capabilities": {
    "streaming": true,
    "pushNotifications": true,
    "stateTransitions": true
  },
  "skills": [
    {
      "id": "freely-fix-execution",
      "name": "Bug Fix Execution",
      "description": "快速修复 bug 的特殊高效策略",
      "inputModes": ["text", "json"],
      "outputModes": ["text", "json"]
    },
    {
      "id": "freely-feat-execution",
      "name": "Feature Execution",
      "description": "新功能/大型改动的完整开发流程",
      "inputModes": ["text", "json"],
      "outputModes": ["text", "json"]
    },
    {
      "id": "freely-doc-B1_IBM-execution",
      "name": "B1_IBM Pre-Research",
      "description": "I→B→M 第一阶段预研收敛"
    },
    {
      "id": "freely-doc-B2_IBM-execution",
      "name": "B2_IBM Design",
      "description": "I→B→M 第二阶段实现设计"
    }
  ],
  "defaultErrorHandlingMode": "agentic",
  "freely": {
    "agentType": "worker",
    "worktreeIsolation": true,
    "worktreeRoot": "/path/to/project-worktrees",
    "supportedExitKinds": [
      "manager_working",
      "worker_working",
      "worker_done",
      "worker_blocked",
      "worker_handoff_needed",
      "delegate_workers",
      "resume_manager",
      "stop_ai"
    ],
    "handoffJsonSchema": "https://freely.dev/schemas/handoff-v1",
    "supportedSkills": [
      "freely-fix-execution",
      "freely-feat-execution",
      "freely-doc-B1_IBM-execution",
      "freely-doc-B2_IBM-execution"
    ],
    "transport": "unix-domain-socket",
    "socketPath": "/tmp/freely-a2a-worker.sock",
    "runtime": {
      "version": "0.1.0",
      "tool": "codex",
      "model": "claude-sonnet-4-7",
      "mode": "auto"
    },
    "projectRoot": "/path/to/project",
    "branch": "feature/xxx"
  }
}
```

## 验证

```bash
# 验证 Agent Card JSON Schema
python3 -c "
import json
import jsonschema

with open('docs/system/workspace/a2a/agent-card-schema.json') as f:
    schema = json.load(f)

# 验证示例
with open('docs/system/workspace/a2a/examples/worker-agent-card.json') as f:
    instance = json.load(f)

jsonschema.validate(instance, schema)
print('Agent Card schema validation passed')
"
```

## 参考

- [A2A Agent Card Specification](https://github.com/A2A-Specification/A2A)
- [JSON Schema Draft-07](https://json-schema.org/draft-07/json-schema-release-notes.html)