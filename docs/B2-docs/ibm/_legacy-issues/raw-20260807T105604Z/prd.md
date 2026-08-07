# PRD: I-20260807T105604Z-A — .codex/config.toml 解除跟踪

## Goal
- 让 `.codex/config.toml` 不再被 git 跟踪；本地文件保留，且本地修改不会污染 develop working tree。

## 非目标
- 不添加 example 模板。
- 不改 clean-tree 检查。
- 不改 `.gitignore`（规则已存在，`.gitignore:78`）。

## 实现方案
- `git rm --cached .codex/config.toml`（解除 index 跟踪，保留本地文件）。
- 提交后 `.codex/` 忽略规则生效，后续本地修改不产生 tracked dirty。

## Dev-Loop Handoff
- 改动面：`.codex/config.toml`（仅解除跟踪）。
- 测试面：test-pre-merge 工位验证 `git ls-files .codex` 为空、`git status --porcelain` 干净、`git check-ignore` 命中 `.gitignore:78`。
