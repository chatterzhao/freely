# Freely A2A 替换 Handoff 架构分析（修正版）

**生成时间**：2026-06-12  
**核心问题**：A2A 与 Handoff 的真正关系是什么？

---

## 一、关键发现

### 1.1 A2A Server 数据存储是内存的

```python
# a2a_server.py
self._tasks: Dict[str, Task] = {}  # 内存字典，无持久化
```

**问题**：进程重启后所有 Task 状态丢失

### 1.2 Handoff 表是 SQLite 持久化的

```sql
-- handoff 表结构
CREATE TABLE handoffs (
    handoff_id TEXT PRIMARY KEY,
    status TEXT,
    exit_kind TEXT,
    reason TEXT,
    ...
);
```

**作用**：持久化 Manager-Worker 状态，支持 daemon 重启后恢复

---

## 二、正确的架构理解

### 当前架构

```
Manager                              Worker
   │                                    │
   ├─ prompt 文件 ──────────────────────▶│  (文件系统)
   │                                    │
   ├─ handoff JSON ──▶ SQLite ──▶ 读取 ◀──│  (数据库)
   │                                    │
   └─ 轮询状态 ◀─────────────────────────│  (轮询)
```

### 正确目标架构

```
Manager                              Worker
   │                                    │
   ├─ A2A create_task() ───────────────▶│  (Unix Socket)
   │                                    │
   ├─ A2A update_task() ◀───────────────│  (SSE Streaming)
   │                                    │
   └─ A2A get_task() ◀─────────────────│  (轮询/推送)
                                            │
                                            ▼
                                      SQLite (持久化)
```

---

## 三、"彻底替换"的真正含义

### ❌ 废弃的部分

1. **Handoff exit_kind 别名逻辑**
   - 30+ 个别名映射（`completed` → `worker_done` 等）
   - 复杂的 fallback 逻辑
   - `completion_summary` 作为 `reason` 的 fallback

2. **Handoff 复杂状态机**
   - 8 种 exit_kind
   - 多种别名变体

### ✅ 保留的部分

1. **SQLite 持久化**
   - Task 状态持久化到数据库
   - 支持 daemon 重启后恢复
   - 可能复用 handoff 表或新建 a2a_tasks 表

2. **Handoff 的设计意图**
   - Manager-Worker 状态传递
   - 任务委派和结果收集

### 🔄 重构的部分

1. **Handoff 表 → A2A Task 表**
   ```sql
   -- 新表结构
   CREATE TABLE a2a_tasks (
       task_id TEXT PRIMARY KEY,
       state TEXT,           -- submitted/working/completed/failed
       skill TEXT,
       prompt_file TEXT,
       worktree TEXT,
       branch TEXT,
       reason TEXT,
       progress TEXT,
       completion_summary TEXT,
       evidence_paths TEXT,
       created_at TEXT,
       updated_at TEXT
   );
   ```

2. **exit_kind → A2A Task State**
   ```
   Freely exit_kind     → A2A Task state
   ─────────────────────────────────────
   manager_working      → submitted
   worker_working       → working
   worker_done          → completed
   worker_blocked       → input-required
   stop_ai              → failed
   ```

3. **文件系统 → A2A Protocol**
   ```
   旧：prompt 文件写入文件系统
   新：A2A create_task() + prompt_file 参数
   ```

---

## 四、A2A 实现必须修复的问题

### 4.1 持久化缺失

**问题**：当前 A2A Server 的 `_tasks` 是内存字典

**修复**：
```python
class A2AServer:
    def __init__(self, project: str):
        self.project = project
        self._tasks: Dict[str, Task] = {}
        self._db = self._init_db()  # SQLite 持久化
    
    def _init_db(self):
        # 创建 a2a_tasks 表或复用 handoff 表
        ...
    
    def _save_task(self, task: Task):
        # 保存到 SQLite
        ...
    
    def _load_task(self, task_id: str) -> Optional[Task]:
        # 从 SQLite 加载
        ...
```

### 4.2 与 Freely Runtime 集成

**问题**：A2A Server 未被 Worker 启动时调用

**修复**：
```bash
# Worker 启动脚本
./bin/freely worker start \
    --project $PROJECT \
    --a2a-server \  # 启动 A2A Server
```

### 4.3 与 ACP Bridge 集成

**问题**：A2A Server 不复用 ACP session

**修复**：
```
Worker 启动流程：
1. 启动 ACP Bridge（claude-agent-acp）
2. 启动 A2A Server（监听 Unix Socket）
3. A2A Server 调用 ACP Bridge 执行任务
```

---

## 五、迁移计划

### Phase 1：数据层迁移

1. 创建 `a2a_tasks` 表（兼容现有结构）
2. A2A Server 写入 SQLite
3. 保留 Handoff 表作为 fallback

### Phase 2：协议层迁移

1. Worker 启动 A2A Server
2. Manager 使用 A2A Client 委派任务
3. 废弃文件系统传递 prompt 方式

### Phase 3：简化

1. 删除 Handoff exit_kind 别名逻辑
2. 删除 Handoff 复杂状态机
3. 只保留 A2A + SQLite

---

## 六、结论

**"彻底替换 Handoff"** 的真正含义：

| 废弃 | 保留 |
|------|------|
| Handoff exit_kind 别名逻辑 | SQLite 持久化 |
| Handoff 复杂状态机 | A2A Protocol |
| 文件系统传递 prompt | Task 状态表（可能是新表） |

**不是**：
- ❌ 完全删除持久化
- ❌ 只用内存存储
- ❌ A2A 替代 SQLite

**而是**：
- ✅ 用 A2A 替代文件系统通信
- ✅ 用 A2A Task State 替代 exit_kind 别名
- ✅ 用 SQLite 持久化 A2A Task 状态

---

*修正版分析*