# PRD: pretests-gate 字段值解析统一化

- issue_id: I-20261104T082740Z-A
- source_raw: raw-20261104T082740Z

## Goal

让 `pretests-gate` 把 `- key: value` 行的**整行剩余内容**当作字段值：Markdown 行内代码反引号、冒号、`$HOME` 都只是内容而不是分隔符；空值明确判为缺失，绝不吸纳下一行；同时完整保留 #3957 建立的「裸值 / 单引号 / 双引号 / 反引号」四格式兼容。所有字段读取路径收敛到同一个真源函数，消除 8 份各自演化的正则。

## 非目标

- 不修改 pre-tests.md 的字段集合、取值枚举、章节结构或门禁失败分类。
- 不把治理文档改成 YAML/JSON 等结构化格式。
- 不修改 `bin/pretests-gate` 转发 shim。
- 不修平台读通道静默返回空清单、raw key 漂移、`raw-issue-pull` 不写一级标题等独立缺陷（各有其 raw issue）。
- 不修 9 个 legacy 门禁测试的断言漂移（已被 `#4151` 覆盖，见 B1 brainstorms §Related findings）。

## 现状与约束

- 真源：`docs/system/workspace/scripts/quality/pretests-gate`（803 行，bash 外壳 + heredoc 内嵌 Python）。`bin/pretests-gate` 为转发 shim。
- 目录分层：`docs/system/workspace/scripts/README.md` 声明 `scripts/` 为系统真源、`bin/` 为运行时投影位置；本项目 `bin/` 是混合结构，`pretests-gate` 属于 shim 类，因此只改 `scripts/quality/`。
- 8 处字段正则及其调用方空值语义见 B1 brainstorms §Decision 表。
- `\s*` 会跨行：Python `re.MULTILINE` 下 `\s` 匹配 `\n`，空值字段后的下一行内容会被 `([^`\n]+)` 捕获成当前字段值。
- #3957 兼容基线：`docs/B2-docs/gate/pretests-gate-field-parsing-compat/raw-20260717T041435Z/issues/I-20260717T041435Z-A.md`（门禁字段解析引号可选化）。本 PR 复用同一 story，不新建 epic/story 节点，`docs/epics-map.svg` 因此无需改动。

## 实现方案

### 1. 唯一真源 `_field_line_value(text, key) -> (present, value)`

```
re.search(rf"^- {re.escape(key)}:[ \t]*(.*)$", text, re.MULTILINE)
```

- `[ \t]*` 严格限制在单行内，根除跨行错读。
- `(.*)` 取该行剩余全部内容；`.` 默认不跨行。
- 仅当首尾为**同一对**引号、且内部不含该引号时剥离外层，兼容 #3957 四格式，同时避免把含多段行内代码的值误剥。
- 返回 `(present, value)`：区分「字段不存在」「字段存在但为空」「字段有值」三种状态。

### 2. 逐调用方保留语义

| 函数 | 统一后的实现 | 语义不变点 |
|---|---|---|
| `phase_state()` | `_field_line_value(text, "phase_state")[1]` | 反引号包裹值仍可取 |
| `parse_issue_binding().extract()` | `_field_line_value(text, field)[1]` | 四格式兼容（#3957） |
| `derive_tasks_path()` | `present, value = ...; if present and value: return value` | 空值回退默认 tasks.md |
| `parse_fields()` | `if present and value: fields[key] = value` | 空值不收录，且不吞下一行 |
| `parse_scalar()` | `_field_line_value(section_text, key)[1]` | 由「不支持单/双引号」补齐为四格式 |
| `has_blocker_taxonomy()` | `_field_line_value(section_text, "blocker_taxonomy")[0]` | 空值行仍算存在 |
| `issue_is_follow_on()` | `bool(present and value)` | 空值不算 follow-on |

保留的两处行内 `\s*` 属于**单行**标题/任务序号匹配（`re.match` 逐行调用），不是字段值解析，不改动。

### 3. 回归测试

新增 `docs/system/workspace/scripts/tests/test-pretests-gate-inline-code-fields`，`unit` 组直接从脚本内嵌 Python 中 exec 出被测函数，覆盖 17 条断言；`e2e` 组在 `mktemp` 隔离 git 仓库里构造含行内代码的完整治理文档并运行真实门禁，断言退出码 0 且无字段缺失报错。

## 验收

见 `verification/pre-tests.md` 的 AT-001，以及 `verification/test-evidence/AT-001-RED.log` / `AT-001-GREEN.log`。
