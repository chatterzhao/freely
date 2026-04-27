# B1_IBM 预研：chat 插话与 issue 统一

## 当前状态

B1_IBM 的 Input 有两个入口：
- **平台 issue**（github/gitee）：`task-source-scan.py` 扫到后路由到 B1
- **chat 插话**：`freely chat` → `.freely/intake/<id>/message.txt` → intake scan → 路由到 B1
- **intake chat**:`freely intake chat`

两者走不同的存储路径，chat 内容不在 issue 体系内。

## 目标

统一 Input source 为 github/gitee issue。chat 插话是 issue 的评论或新 issue 的创建方式。本地以 issue 为单位组织所有内容，平台 issue 是唯一真相源（本地是缓存 + 离线缓冲）。

## 设计问题

### 1. 本地 issue 存储结构

```
.freely/issues/
├── ISSUES.md                # 索引：所有已知 issue 的映射表
├── {issue-local-id}/
│   ├── meta.env             # 平台 ID、状态、关联 milestone issue
│   ├── issue.md             # 本地 issue 内容
│   └── comments/
│       ├── {timestamp}.md   # 每条评论一个文件
│       └── ...
```

`ISSUES.md` 索引记录：
- `local_id`：本地唯一 ID
- `platform_ids`：`github:<owner>/<repo>#<num>, gitee:<owner>/<repo>#<num>`
- `kind`：`raw`（原始 issue，B1 输入）/ `linked`（里程碑 issue，B2 产出）/ `inbox`（未归类插话）
- `canonical_issue_path`：B2 产物的 issue 路径（linked 类型）
- `sync_state`：每个平台的同步状态

### 2. chat 插话的 issue 路由

用户在终端 `freely chat "xxx"` 时，需要决定这条消息属于哪个 issue：

```
freely chat "xxx"
    │
    ├── 消息命中已有 issue？
    │   ├── 是 → 作为该 issue 的评论写入
    │   └── 否 → 新建 raw issue，消息为 issue body
    │
    ├── 如何判断"命中已有 issue"？
    │   ├── 用户在消息中显式引用 issue（#123、issue-abc）
    │   ├── AI 判断消息内容与已有 issue 相关
    │   └── 默认：写入 inbox issue，后续 AI 归类
    │
    └── 紧急？
        ├── 消息命中的 issue 正在 dev-loop 中 → 标记 urgent，触发通知
        └── 否则 → 不做特殊处理，等待 scan
```

### 3. 两种 issue 类型

沿用现有设计中的二分法：

| | raw issue | linked issue |
|---|---|---|
| 来源 | 用户直接创建（平台 or chat） | B2_IBM 产出，freely 创建 |
| 状态 | 未与 canonical docs 关联 | 已关联 `docs/epics/.../issues/` |
| scan 行为 | `restart_point=pre_brainstorm` | `restart_point=cleanup` |
| 用户评论 | 自由评论 | 评论触发 drift reconcile |
| 关闭时机 | B2 完成后由 freely 关闭 | 不需要关闭（或跟随 canonical completion） |

### 4. 用户直接评论已关闭的 raw issue

场景：raw issue 已被 freely 处理完毕（B1→B2→merge→cleanup），raw issue 已关闭。用户又在平台上评论了这个 issue。

行为：
- sync 脚本拉取评论到本地
- scan 发现 `linked_open_issue` + 新评论 → `restart_point=cleanup`
- AI 判断评论内容：是否需要 reopen？是否为新的 discovery？
- 如果是新 discovery → 创建新的 raw issue，引用原 issue 上下文

### 5. 紧急机制

某些 chat 内容需要更快让 AI 看到（比如纠正错误、提级）。

判断紧急的标准：消息命中的 issue 是否正在 dev-loop 中。

```
if issue 的 phase_state in {in_dev, in_verification}:
    → 写入评论后立即触发 runtime signal
    → supervisor 在下一次 keepalive 检查时发现 signal
    → 中断当前 worker，处理紧急评论
else:
    → 写入评论，等待下次 task-source-scan 自然扫到
```

### 6. 多平台同步

```
本地脚本 issue-sync：
    push：本地有变更的 issue/评论 → 推到配置的平台
    pull：平台上新的 issue/评论 → 拉到本地
    冲突：平台和本地都有新评论 → 两边都保留，按时间戳排序

平台优先级：
    - 如果 github 和 gitee 都配置了 → 主平台 push，副平台 mirror
    - 默认主平台按 remote 检测
```

### 7. UI 概念

简单 TUI 层：
- 显示当前活跃的 issue（正在 dev-loop 中的）
- 每个 issue 下有一个评论输入区
- 评论自动带 issue local_id
- 紧急标记：勾选"需要 AI 立即处理"

### 8. chat 命令变化

当前命令：
```
freely chat <message>              # 通用插话
freely chat --message-file <path>  # 文件插话
```

变更后：
```
freely chat <message>                           # 默认写入 inbox issue
freely chat --issue <id> <message>              # 指定 issue
freely chat --issue <id> --urgent <message>     # 紧急插话
freely chat --new-issue <message>               # 显式创建新 issue
```

## 未解决问题

1. **inbox issue 何时由谁归类？** AI 定期扫描 inbox，将消息分配到正确的 issue。频率是多少？
2. **issue local_id 用什么格式？** UUID？递增数字？`raw-YYYYMMDD-NNNN`？
3. **现有的 `.freely/intake/` 目录是否废弃还是迁移？**
4. **sync 脚本是 daemon 自动跑还是手动触发？**
5. **评论是否需要 session_refs 追踪？** 一条评论可能来自 AI worker 的发现、用户的 chat、或平台上的第三方用户——来源不同，处理方式不同。

## 决定

暂不在此 brainstorms.md 中做决定。先列出所有需要收敛的问题，下一步产出 candidates.md。
