# Freely 项目治理入口

> 本文件由 Claude Code 自动加载。完整治理规则请见 [AGENTS.md](./AGENTS.md)。

## 权威来源（优先级）
1. `docs/CONSTITUTION.md` — 硬性约束
2. `docs/LAWS.md` — 操作规则
3. `docs/PROJECT_INTENT.md` — 产品方向
4. `AGENTS.md` — 开发流程入口

## 关键约束

以下行为 **绝对禁止**（来自 CONSTITUTION.md §5）：
- `git -c core.hooksPath=/dev/null` — 禁用 hook
- `git push --force` 到 `main` 或 `develop`
- `--no-verify` / `--no-gpg-sign` — 跳过 hook
- 直接在 `main`/`develop` 上 `git commit`
- 修改 `.githooks/` 内容以削弱检查

## 标准开发流程
```
feedback/scan → wt-create → B1_IBM → B2_IBM → dev → test-pre-merge → pr-create-guarded → pr-review-guarded → pr-merge-guarded → wt-close
```

## 会话启动检查
1. 检查分支：禁止在 `main`/`develop`/`test-pre-merge-*` 上直接写入
2. 使用 `./bin/wt-create` 创建 feature worktree
3. 确认 `git config --get core.hooksPath` 返回 `.githooks`

## 核心原则
- **代码先行，治理后置**：先改源码验证，再补 IBM 文档
- **封装命令优先**：使用 `pr-create-guarded` 等封装命令，禁止原子 `git push`/`git merge`
- **Freely 自举**：开发 Freely 时优先使用 Freely 自己的 skill/runtime
