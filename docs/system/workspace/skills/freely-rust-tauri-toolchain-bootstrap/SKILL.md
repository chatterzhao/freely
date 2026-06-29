---
name: freely-rust-tauri-toolchain-bootstrap
description: >- 基于 Rust/Cargo/Tauri 官方机制和 rsproxy 镜像完成可复用的 toolchain
  bootstrap。处理 rustup 下载不稳定或缺少 cargo/rustc 的情况。

  Use when: Rust/Tauri 项目缺少工具链或默认 rustup 下载失败。
  触发词："rustup"、"cargo"、"toolchain"、"tauri build"、"rsproxy"。
---

# skill:freely-rust-tauri-toolchain-bootstrap

## 何时使用

- `cargo`、`rustc`、`rustup` 任一缺失
- `rustup` 默认源下载失败或很慢
- 当前任务需要继续 `cargo check`、`cargo test`、Tauri 编译验证

## 工作流

1. 先验证代理链路可达。
   - `curl --max-time 30 https://rsproxy.cn/index/config.json`
   - `curl --max-time 30 https://rsproxy.cn/rustup-init.sh`
   - 需要具体平台二进制时，再测 `https://rsproxy.cn/rustup/dist/<target>/rustup-init`

2. 默认绕开本机代理，直连镜像。
   - 安装和验证阶段优先执行：
   - `env -u HTTP_PROXY -u HTTPS_PROXY -u ALL_PROXY -u http_proxy -u https_proxy -u all_proxy ...`
   - 只有直连镜像失败时，才允许重新评估是否需要走本机代理

3. 配置 rustup 镜像环境变量。
   - `export RUSTUP_DIST_SERVER=https://rsproxy.cn`
   - `export RUSTUP_UPDATE_ROOT=https://rsproxy.cn/rustup`

4. 为项目写入或更新 `.cargo/config.toml`。
   - 优先使用 Cargo 官方支持的 sparse registry / source replacement / net 配置
   - 保留项目已有的其他 Cargo 配置，不要覆盖无关项
   - 具体片段见 [rsproxy.md](references/rsproxy.md)
   - 官方依据见 [official-guidance.md](references/official-guidance.md)

5. 安装 Rust toolchain。
   - `env -u HTTP_PROXY -u HTTPS_PROXY -u ALL_PROXY -u http_proxy -u https_proxy -u all_proxy RUSTUP_DIST_SERVER=https://rsproxy.cn RUSTUP_UPDATE_ROOT=https://rsproxy.cn/rustup bash -lc 'curl --proto "=https" --tlsv1.2 -sSf https://rsproxy.cn/rustup-init.sh | sh -s -- -y'`
   - 然后执行 `source "$HOME/.cargo/env"`
   - 若现有 `~/.rustup` 已半损坏，先备份而不是反复硬修：
   - `mv ~/.rustup ~/.rustup-broken-$(date +%Y%m%d-%H%M%S)`
   - 再创建新的 `~/.rustup` 并重跑安装

6. 立刻回归。
   - `bun run rust:preflight`
   - `bun run cargo:check:probe`
   - 如仓库有更高层验证，再继续跑对应 Rust/Tauri 测试

7. 失败时不要空转。
   - 若 `rsproxy` 不可达：记录为环境阻塞
   - 若 rustup 安装失败：记录失败点、下载 URL、下一步重试建议
   - 若 rustup 本地状态损坏并报 manifest/rename 错误：备份旧 `~/.rustup`，重新初始化，不要在坏状态上反复重试
   - 若报 package cache lock：先确认是否有其他 Cargo 进程，再决定等待还是终止冲突进程
   - 若 toolchain 装好但 `cargo check` 失败：回到真实编译错误，不再继续把 blocker 写成环境缺失

## 边界

- 这个 skill 解决的是 toolchain bootstrap，不负责长期磁盘治理
- `CARGO_HOME`、`target/`、编译缓存复用属于后续独立能力
- 若当前问题已从“环境缺失”转为“真实编译错误”，立即退出本 skill，回到对应 Rust/Tauri issue 的正常开发环

## 完成标准

- `cargo`、`rustc`、`rustup` 都可执行
- 项目级 Cargo 源配置明确
- 至少一条 Rust 编译相关命令真实执行
- continuity artifact 反映最新验证结果

## References

- [rsproxy.md](references/rsproxy.md)
- [official-guidance.md](references/official-guidance.md)
