# Official Guidance

## Rust / Cargo

- Cargo Home 官方说明：`CARGO_HOME` 是下载和源码缓存，默认在 `~/.cargo/`
  - https://doc.rust-lang.org/cargo/guide/cargo-home.html
- Cargo 配置官方说明：支持项目级或全局 `.cargo/config.toml`
  - https://doc.rust-lang.org/cargo/reference/config.html
- 官方配置中可用：
  - `registries.crates-io.protocol = "sparse"`
  - `source.<name>.replace-with`
  - `build.target-dir`
  - `build.rustc-wrapper`
  - `net.git-fetch-with-cli`
- Build cache 官方说明：
  - 默认构建产物在项目 `target/`
  - 可通过 `CARGO_TARGET_DIR` 或 `build.target-dir` 调整
  - 第三方 `sccache` 可共享不同 workspace 的编译缓存
  - https://doc.rust-lang.org/cargo/reference/build-cache.html
- rustup 环境变量官方说明：
  - `RUSTUP_DIST_SERVER`
  - `RUSTUP_UPDATE_ROOT`
  - https://rust-lang.github.io/rustup/environment-variables.html

## Tauri

- Tauri 官方 prerequisites 明确要求 Rust，并默认指向 rustup 安装路径
  - https://v2.tauri.app/start/prerequisites/
- Tauri 官方并没有单独规定国内镜像方案，因此镜像属于在 Rust 官方机制之上的环境适配层，而不是 Tauri 私有能力。

## 结论

1. 官方长期机制是：
   - rustup 管工具链
   - Cargo Home 管下载缓存
   - `target/` 管项目构建产物
2. 对 Freely 最值得标准化的不是“发明新依赖系统”，而是：
   - 固定 `rustup + Cargo config` 的官方扩展点
   - 在网络受限环境下给出稳定镜像实现
   - 把 `target/` 和编译缓存治理单独作为后续能力
