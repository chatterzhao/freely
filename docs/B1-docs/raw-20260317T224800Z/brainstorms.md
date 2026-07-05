# 20260317-2248 Rust Toolchain Bootstrap Skill

## 背景

本轮 dogfooding 已确认：

- `I-20260317T100500Z` 的真实 blocker 不是边界不稳，而是本机缺少 `cargo/rustc/rustup`
- 默认 `sh.rustup.rs` 在当前网络环境下不稳定
- `rsproxy` 的关键链路已经实测可用：
  - `https://rsproxy.cn/rustup-init.sh`
  - `https://rsproxy.cn/index/config.json`
  - `https://rsproxy.cn/rustup/dist/aarch64-apple-darwin/rustup-init`

这类问题会反复出现在 Freely 自举和其他 Rust/Tauri 项目中，不应该继续只留在 continuity 文档里。

## 判断

应把“Rust/Tauri toolchain 缺失时，如何在当前网络环境下完成可复用的镜像配置、安装与回归验证”沉淀成正式 skill，而不是继续依赖一次性聊天说明。

## 预期能力

skill 至少应覆盖：

1. 何时触发
   - 缺少 `cargo/rustc/rustup`
   - `rustup` 默认下载失败
   - Rust/Tauri 项目首次机器 bootstrap

2. 最小步骤
   - 验证 `rsproxy` 可达
   - 配置 `RUSTUP_DIST_SERVER` / `RUSTUP_UPDATE_ROOT`
   - 配置项目级 `.cargo/config.toml`
   - 安装 rustup/toolchain
   - 重新加载 `~/.cargo/env`
   - 回跑预检与 `cargo check`

3. 失败分支
   - `rsproxy` 不可达时记录阻塞
   - 稀疏索引可达但 rustup 失败时降级到逐步下载重试
   - 安装后仍失败时要求回写 continuity artifact

## 落点

- `docs/system/workspace/skills/rust-tauri-toolchain-bootstrap/`
- `bin/check-rust-toolchain`
- `src-tauri/README.md`

## 为什么值得 skill 化

- 这是高频且脆弱的环境问题
- 顺序和参数有明确最佳实践，适合低自由度流程
- 与 Freely 的 `CLI First`、非交互、自举复用高度一致
