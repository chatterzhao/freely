- issue_id: I-20260514T103532Z-A
- issue_path: docs/issues/I-20260514T103532Z-A/issue.md

## Implementation Decision Note

- decision: AI 不再直接调用 handoff.py update/insert（CLI 命令），改为在回复末尾输出 ```handoff JSON 块，由 Runtime 统一解析、验证、合并字段后写入 DB 并分发消费。
- why_this: 当前 AI 分步执行 CLI 命令（Step B handoff.py update 写 manager exit contract，Step C handoff.py insert 逐条创建 worker 记录）之间无原子性保证——Step B 做了 Step C 没做会导致 validator 读 worker_prompts_csv 为空、launcher 读 pending worker 也为空（#343）。AI→JSON→Runtime 模型下，AI 只输出一个 JSON，Runtime 做唯一一次解析写入——不存在分步不一致的可能性。另外，JSON 格式比 CLI 参数列表更适合 AI 输出，CLI 的 5 个字段映射到单一的 reason 字段后，JSON 的 key-value 结构更自然。
- alternatives_considered: 1. 保持 CLI 但加事务——handoff.py 内用 SQLite 事务包裹 insert+update，但 AI 分步调用 CLI 不在同一进程内，事务无法跨进程。排除。2. AI 直接写 SQLite——安全风险（SQL 注入）、schema 耦合。排除。3. gRPC/HTTP API——引入新依赖、新端口、新认证。过度设计。```handoff 代码块复用现有 AI reply 文本通道，零新增依赖。
- boundary_non_goals: JSON 块格式固定为 ```handoff，不与 ```json 通用代码块混淆。Runtime 管理的字段（18 个）不在 JSON 中出现——AI 只输出它负责的 7 个。验证失败不抛异常——插入结构化修复 handoff，Manager 下轮 patrol 处理。不改变 Manager/Worker 的 patrol 循环结构——只改变 exit 时的输出方式。
- residual_risk: AI 可能不输出 JSON 块——Runtime 检测到缺失，插入修复 handoff，Manager 处理。有兜底。JSON 格式正确但内容错误（如 worker_prompts_csv 指向不存在的文件）——Runtime 验证路径存在性，不达标则修复 handoff。有兜底。Agent doc 本身写错（如 JSON 示例格式有语法错误）——Manager/Worker 按错误示例输出，反复验证失败，需要人工修 doc。无自动兜底；缓解措施：agent doc 的 JSON 示例在 pre-tests 中验证可 parse。
