---
b1_id: B1-20260807T114900Z
phase_state: completed
source_raw: raw-20260807T114900Z
source_url: https://github.com/chatterzhao/freely/issues/4107
produced_candidate: C-20260807T114900Z-A
created_at: 2026-08-07T12:00:00Z
---

# B1_IBM: task-lifecycle-scan platform_adapter import 断裂导致 scan 降级

## Input

- **来源**: GitHub #4107 / Gitee IK787N，P0。`freely task-source-scan --json` 报 `platform_health: degraded`，reason=`No module named 'platform_adapter'`，total=0。**87 个 open platform issues（50 gitee + 37 github）对 scan 不可见**。
- **涉及文件**: `docs/system/workspace/scripts/runtime/task-lifecycle-scan.py`（L451 `_detect_platforms`、L502 `get_platform_open_issues`、L548 `get_all_platform_issue_states` 三处直接导入）
- **真源**: `docs/system/workspace/scripts/sync/platform-adapter.py`（文件名带连字符）

## Problem

### 现象
`task-lifecycle-scan.py` 三处直接写 `from platform_adapter import ...`，但模块文件名是 `platform-adapter.py`（连字符）。Python import 系统按模块名解析，`platform_adapter` 无法解析为磁盘文件 → ImportError。

- `_detect_platforms` 捕获异常后回退到 git remotes（平台仍能识别，掩盖了根因）
- `get_platform_open_issues` 捕获异常后返回 `{"__degraded__": ...}` → scan 标记 `platform_health: degraded`，平台 issue 全量不可见

### 根因拆解

#### R1: 模块名与文件名不一致
文件名为 `platform-adapter.py`（连字符是刻意约定，避免与 pip 安装的 `platform_adapter` 包冲突），但调用方用 `platform_adapter`（下划线）导入。连字符不是合法 Python 标识符，`import platform_adapter` 必然失败。

#### R2: 三处导入各自 `sys.path.insert` 且重复
L451/502/548 每次都 `sys.path.insert(0, <sync 目录>)` 再 import，路径作用域不隔离，失败路径不一致——`_detect_platforms` 有 fallback，其余两处没有。

#### R3: 治理链断裂 — 之前的修复从未落地
- `raw-20260623T022909Z`（#3380）覆盖同一 bug，标记 `absorbed` → `I-20260623T022909Z-A` 标记 `completed`，平台 issue 关闭
- 真实代码修复 commit `2b2f4c77f`（importlib `_get_pa()` loader）**orphaned，从未 merge 到 develop**
- `3d67e39a1` 只物化了 issue 文档并 `Closes #3380`，没碰 task-lifecycle-scan.py → phantom closure：issue 关了，bug 还在

### 覆盖域
- `task-lifecycle-scan.py` 三处导入点 + 顶部 imports
- `platform-adapter.py` 被加载后自身依赖（`freely_user_env`、`freely_config`，模块内部已自行把 adapter/runtime 目录加入 sys.path）
- 不在本 issue 范围：`platform-adapter.py` 本身逻辑、其它消费 `platform-adapter.py` 的脚本

## Brainstorm

### Option A: importlib 加载器 `_get_pa()`（推荐）

在 `task-lifecycle-scan.py` 顶部加 `import importlib.util`，新增缓存加载器：

```python
def _get_pa(project: Path):
    global _PA_MODULE, _PA_PROJECT
    sync_dir = project / "docs" / "system" / "workspace" / "scripts" / "sync"
    if _PA_MODULE is None or _PA_PROJECT != project:
        spec = importlib.util.spec_from_file_location(
            "platform_adapter", str(sync_dir / "platform-adapter.py"))
        _PA_MODULE = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(_PA_MODULE)
        _PA_PROJECT = project
    return _PA_MODULE
```

三处替换为 `_get_pa(project).configured_platforms()` / `.list_open_issue_records()` / `._handlers(), ._safe`。

- 复用 orphaned commit `2b2f4c77f` 的先例设计，但针对**当前结构**重写（旧代码用 `Path(__file__).parent.parent / "sync"`，当前是 `project / "docs" / "system" / "workspace" / "scripts" / "sync"`；旧符号 `list_open_issues`/`fetch_issue_state` 已重命名为 `list_open_issue_records` 等）
- 优点：改动局限单文件；不触碰 `platform-adapter.py` 及外部引用；加载后平台逻辑与直接 import 等价
- 缺点：`_PA_MODULE` 全局缓存需要按 project 失效（同进程多 project 场景）

### Option B: 重命名 `platform-adapter.py` → `platform_adapter.py`

统一文件名，直接 `import platform_adapter` 恢复。

- 缺点：文件名连字符是刻意约定（防包名冲突）；全仓所有 `platform-adapter.py` 路径引用（bin、runtime freely、其它脚本）都要同步改名；改名后 `Path(__file__)` 相对路径逻辑不变但引用方风险面大。评估：改动面失控，否决。

### Option C: sync/ 目录新增 shim `platform_adapter.py`

`from platform_adapter import *` 变成 shim 再转发。

- 优点：不碰 scan
- 缺点：新增文件 + import 解析链变长，且 shim 加载真实模块仍需 importlib（把问题藏起来）。评估：过度设计，否决。

## Decision: Option A

**理由**:
- 根因是"模块名与文件名不一致"，importlib `spec_from_file_location` 直接按真实文件加载，是最贴近根因的修复
- 有 prior art（orphaned commit `2b2f4c77f`），设计已被验证过，只差按当前结构重写落地
- 改动面最小：单文件三处 + 一个 helper，`platform-adapter.py` 零改动
- 与"文件名带连字符"的刻意约定兼容，不破坏其它消费方

**具体实现**:
1. 顶部加 `import importlib.util`
2. 新增缓存 `_get_pa(project)` helper（`spec_from_file_location` + `module_from_spec` + `exec_module`，按 project 缓存失效）
3. L451 `_detect_platforms` → `_get_pa(project).configured_platforms()`
4. L502 `get_platform_open_issues` → `_get_pa(project).list_open_issue_records()`
5. L548 `get_all_platform_issue_states` → `_get_pa(project)._handlers()` / `_get_pa(project)._safe`

## Candidate

- candidate_id: `C-20260807T114900Z-A`
- status: promoted
- milestone: `M-20260807T114900Z-A`
