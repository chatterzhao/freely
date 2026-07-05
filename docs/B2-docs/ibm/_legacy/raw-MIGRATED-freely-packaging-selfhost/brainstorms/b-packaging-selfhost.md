# B2 Brainstorm: Freely 打包与自举验证

- I-*: I-20260502-0500-A
- source_candidate: `docs/B1-docs/raw-20260502/candidates.md#C-20260502-0500-A`
- 日期: 2026-05-20

## B1 已收敛的决策

1. **通过 allowlist 打包 workspace 能力文件** — 不打包整个 repo，减少产物体积，避免开发文档泄露
2. **自举验证作为 merge 门禁** — 打包版本能正常完成 Manager cycle 才允许 merge 到 develop
3. **版本号双轨制** — nightly (YYYYMMDD-nightly) 从 develop 出，stable (YYYY.MM.DD-stable) 从 main 出
4. **不做自动 CI 发布** — nightly 发布由 runner 驱动，不纳入仓库代码

## 实现设计

### 打包脚本 (`bin/freely-package`)

```
Usage: freely-package --version <ver> [--output <dir>]
```

**流程:**

1. 解析 `--version` 和 `--output` 参数
2. 读取 `docs/system/workspace/package-allowlist.txt` 作为打包清单
3. 复制 allowlist 中所有路径到 `<output>/<ver>/` 目录，保持相对路径结构
4. 写入版本文件 `<output>/<ver>/FREELY_VERSION`
5. 完整性验证：检查 allowlist 中每个路径在源仓库是否存在；检查复制后文件数是否匹配
6. 输出打包摘要

**关键实现细节:**

- allowlist 支持注释（`#` 开头）和空行
- 允许使用 `-` 行表示目录通配（复制目录下所有文件）
- 复制使用 `rsync -R` 保持相对路径
- 失败时返回非零退出码

### 打包清单 (`docs/system/workspace/package-allowlist.txt`)

清单定义 Freely 产品交付内容——AI 自主开发所需的最小能力集。

分层结构：
1. **核心 workspace 文档** — IBM 框架、三循环契约、agent/skill 定义等
2. **入口脚本** — `bin/` 下所有入口脚本
3. **Git 门禁** — `.githooks/` hook 包装层
4. **初始化模板** — `templates/` Freely init 模板
5. **Tool 边界引导** — `.freely/tool-boundary-bootstrap.md`

不打包的内容通过 `#` 注释在 allowlist 中标明排除理由。

### 自举验证门禁 (`bin/test-pre-merge-selfhost`)

```
Usage: ./bin/test-pre-merge-selfhost [--package-dir <dir>] [--timeout <seconds>]
```

**流程:**

1. 调用 `bin/freely-package` 从当前 develop HEAD 打包
2. 安装打包版本到临时目录
3. 启动 Freely daemon
4. 验证 daemon 健康状态（`freely doctor`）
5. 触发一个完整的 Manager cycle（patrol → 判断 → 产出）
6. 验证 Manager cycle 日志包含预期 stage 输出
7. 正常停止 daemon
8. 清理临时目录
9. 全部通过 → 返回 0；任何步骤失败 → 返回非零并输出错误摘要

**验证项:**

| # | 检查项 | 预期 |
|---|--------|------|
| 1 | `freely doctor` | 全部 PASS |
| 2 | Daemon 启动 | 进程存活，端口监听 |
| 3 | Manager cycle | patrol → 判断 → 产出三个 stage 均完成 |
| 4 | Daemon 停止 | 正常退出，无僵尸进程 |

### 版本号规则

```
nightly:  YYYYMMDD-nightly    # 每天从 develop HEAD 出，一天一个
stable:   YYYY.MM.DD-stable   # 从 main 出，对应正式发布
```

test-pre-merge 批次是一次性验证容器，不产生持久版本。每次自举验证从当前 develop HEAD 打包，版本格式为 `YYYYMMDD-NNN-dev`（NNN 为当天序号）。

## 替代方案评估

| 方案 | 优点 | 缺点 | 结论 |
|------|------|------|------|
| **A) Allowlist 复制** | 精确控制产物；易审计；增量友好 | 需随 workspace 结构维护 | ✅ 采用 |
| **B) 全量 git archive** | 实现简单；天然完整 | 包含开发文档/治理文件；体积大 | ❌ 否决 |
| **C) 符号链接开发树** | 零复制；即时可用 | T0 不稳定；无法验证缓存独立性 | ❌ 否决 |
| **D) Docker 镜像** | 环境隔离好 | 依赖 Docker；增加复杂度；Freely 场景过重 | ❌ 否决 |

## 验收标准细化

### 打包正确性
- 允许清单中所有文件都被复制
- 产物版本号正确
- 产物中 `FREELY_VERSION` 内容与 `--version` 参数一致
- 遗漏 allowlist 文件导致打包失败

### 自举验证
- `freely doctor` 全部 PASS
- Daemon 能正常启动和停止
- 打包版本能完整执行 Manager cycle
- 失败路径报告清晰错误

### 边界条件
- allowlist 为空 → 打包空目录但成功
- allowlist 引用不存在路径 → 打包失败，报错
- 版本号格式不合法 → 打包失败，提示格式要求
- 输出目录不存在 → 自动创建
- daemon 启动超时 → 超时报错，退出码非零

## 不负责

- 不实现 nightly 自动发布 CI
- 不处理用户项目的打包（仅打包 Freely 自身）
- 不处理版本升级迁移
- 不验证缓存优化效果（仅验证功能正确性）
