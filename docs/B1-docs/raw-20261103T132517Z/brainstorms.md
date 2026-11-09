# Brainstorms: raw-20261103T132517Z

## 问题

同一份 issue frontmatter 有 3 套解析器、2 套写入路径，没有唯一所有者；规范实现存在但运行时不用它，解析失败一律静默返回 `{}`。

## 证据（本机实测）

- `task-lifecycle-scan.py` 的 `parse_frontmatter()` 手写切片 + `yaml.safe_load` + `except Exception: pass`，再用手写行解析兜底；损坏文档得到空 `phase_state`，被归入「状态不对齐」类目而非报错。
- `bin/issue-sync` 的 `_fm_get` / `_fm_set` / `_fm_has_key` 内联 `python3 -c` + `2>/dev/null || true`，33 处调用；同文件另有 `_raw_effect` 走规范路径。
- 规范实现 `raw_metadata_contract.read_issue()` 对非法 YAML 抛 `yaml.ParserError`（不是 `MetadataValidationError`），无法被统一捕获。
- 存量坏数据实测：`docs/B1-docs` 下 11 个 `platform_state: closed---`（闭合分隔符粘字段）、1 个含两组 git 冲突标记 + glued 分隔符的 `raw-20260519T145435Z/issue.md`；严格解析共 12 个失败。

## 证伪

- #4183（R13）是 B2 文档路径解析；#4184（R12）是关闭路径顺序；#4216（R12.5）是 test-gate 命令；#4151（R17）是测试证据链。均不涉及 frontmatter 解析所有权。
- open issue 无 `frontmatter 解析 / SDD / yaml.safe_load` 相关项（除本条）。

## 关键设计

1. **契约模块成为唯一真源**：新增 `validate_issue_text()` / `parse_issue_text()` / `validate_issue_path()`；`read_issue()` 把 YAML 异常包装成 `MetadataValidationError`。
2. **scan 不再静默**：`parse_frontmatter()` 调用 `parse_issue_text()`，失败返回 `__metadata_validation_error__` 标记，`read_issues_dir()` 把它填进已有的 `metadata_validation_error` 字段。
3. **issue-sync 薄封装**：`_fm_get` / `_fm_set` / `_fm_has_key` 改为调用 `frontmatter_contract_cli.py`（同一契约模块），删除内联 YAML 解析；调用面 33 处不变。
4. **CLI 统一读写**：`get` / `has-key` / `set` / `check` / `repair`；`set` 优先 `write_issue()`，历史文档字段不全时回退到同一模块的原子写。
5. **存量修复幂等**：`repair` 默认 dry-run、`--apply` 原子写；修 glued 分隔符（只修首个，不受正文水平线干扰）与冲突标记（保留 HEAD 侧并把 `- key: value` 归一化成 YAML 键）。实测 12 个文件修完后再跑为 0，全量 B1 严格解析失败数 0。

## 被否决

在 scan 里再加一层 try/except（仍静默）；让 `read_issue` 直接变成严格解析（会打断大量既有读取路径）；手工逐个改 12 个文件（不可复现）；只修数据不收口解析所有权（必然复发）。
