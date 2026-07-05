# 架构审视：Freely Issue 生命周期管理系统

## 全局视角

Freely 通过抽象 issue 来管理任务全生命周期，形成了闭环系统：

```
平台 (GitHub/Gitee)         本地 (docs/issues/)          人类
     │                          │                        │
     │  issue-sync pull         │  freely chat           │
     │  ──────────────→    raw-YYYYMMDD-HHMM    ←────────│
     │                     kind=raw                    │
     │                          │                        │
     │                     B1 预研                       │
     │                     pre-brainstorms/              │
     │                          │                        │
     │                     C-YYYYMMDD-HHMM              │
     │                     candidate                    │
     │                          │                        │
     │  issue-sync promote      │                        │
     │  ←──────────────    I-YYYYMMDD-HHMM              │
     │  (创建 I-* issue)   kind=linked                  │
     │  (关闭 raw issue)   phase_state=in_b2_ibm        │
     │                          │                        │
     │                     B2 实现 → 验证                │
     │                          │                        │
     │  issue-sync comment      │  freely chat --issue   │
     │  ←──────────────    ### comment-xxx    ←────────│
     │  (平台评论)         (本地评论)          (人类插话) │
     │                          │                        │
     │  issue-sync close        │                        │
     │  ←──────────────    phase_state=completed        │
     │  (关闭 I-* issue)   全部评论已同步               │
     │                     GitHub+Gitee 都 CLOSED        │
```

## 五个核心设计原则

### 1. 时间戳即身份
raw-YYYYMMDD-HHMM / C-YYYYMMDD-HHMM / I-YYYYMMDD-HHMM 共享同一时间戳。
门禁用完全匹配验证 raw→C→I 链。

### 2. 平台是镜像，本地是真相
本地 `docs/issues/` 是唯一权威源。平台数据丢失可从本地重建。
AI 永远不直接读/写平台——`issue-sync` 和 `task-source-scan` 是唯一桥梁。

### 3. 人类通过评论介入
`freely chat --issue I-xxx "修正建议"` → 本地 comment → sync 到平台评论。
评论永远不写入 issue description，只作为平台原生"评论"。
人类和 AI 通过评论协作——这是 process correction 的机制。

### 4. 多平台不锁定
所有操作（create/comment/close）对称推到 GitHub+Gitee。
Pull 时从两边拉取、去重、合并。平台只是通道，不绑定。

### 5. 本地保留完整数据
即使平台全部丢失，本地 `docs/issues/` + `docs/B1-docs/raw-` + `docs/epics/` 包含完整的 issue 生命周期数据。可从本地 `issue-sync create` 重建平台。

## 需要更新的文档

### 高优先级
1. **three-loop-capability-lifecycle.md**（148 行）
   - 补充 raw issue 作为信号入口
   - 补充 platform sync（pull/push）在 auto-loop 中的位置
   - B2_IBM materialization 补充：C-* → I-* 的 promote 动作
   - completion verification 补充：平台 issue close 检查

2. **ibm-framework.md**
   - 示例 ID 改为 HHMM 格式（替换 `0000`）
   - 补充 raw→C→I 身份链说明
   - 补充评论规范（本地主键 + 平台回写）

### 中优先级
3. **session-lifecycle-protocol.md**
   - 补充 session fork 与 worker 上下文继承的最终设计
   - 补充 FORCE_FRESH 标记机制

4. **AGENTS.md**
   - 文件规模部分可能需要更新（如果有新增文件）

### 低优先级  
5. **governance-merge-gate**
   - 新增 GATE 6.3：raw→I 身份链完整性

## B1 候选任务清单（按优先级）

| ID | 内容 | 涉及文件 | 优先级 |
|----|------|---------|--------|
| C-1 | 统一生命周期 Scan 模块 (task-lifecycle-scan.py) | task-source-scan.py, session-cache.sh | P0 |
| C-2 | 修复 I-* ID 格式为 HHMM（新创建） | ibm-framework.md, AI prompt, gate | P0 |
| C-3 | 四层防重：issue+comment push/pull | issue-sync, session-cache.sh | P0 |
| C-4 | 更新 three-loop 图：raw + platform sync + promote | three-loop-capability-lifecycle.md | P0 |
| C-5 | ibm-framework.md 示例改为 HHMM + 评论规范 | ibm-framework.md | P1 |
| C-6 | issue-sync comment：推送+回写 platform_ids | bin/issue-sync | P1 |
| C-7 | 门禁扩展 raw→C→M→I 链 (GATE 6.3) | governance-merge-gate | P1 |
| C-8 | issue-sync pull：平台→本地 issue+评论 | bin/issue-sync | P2 |
| C-9 | 多平台评论去重合并 | bin/issue-sync pull | P2 |
