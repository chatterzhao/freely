# RsProxy Bootstrap

## 推荐环境变量

```bash
export RUSTUP_DIST_SERVER=https://rsproxy.cn
export RUSTUP_UPDATE_ROOT=https://rsproxy.cn/rustup
```

## 推荐安装命令

```bash
env -u HTTP_PROXY -u HTTPS_PROXY -u ALL_PROXY -u http_proxy -u https_proxy -u all_proxy \
  RUSTUP_DIST_SERVER=https://rsproxy.cn \
  RUSTUP_UPDATE_ROOT=https://rsproxy.cn/rustup \
  bash -lc 'curl --proto "=https" --tlsv1.2 -sSf https://rsproxy.cn/rustup-init.sh | sh -s -- -y'
source "$HOME/.cargo/env"
```

## 本地状态损坏时的恢复

若 `rustup show` 报 manifest 缺失，或反复出现 rename/Directory not empty 之类错误，先备份旧状态，再重装：

```bash
mv ~/.rustup ~/.rustup-broken-$(date +%Y%m%d-%H%M%S)
mkdir -p ~/.rustup
env -u HTTP_PROXY -u HTTPS_PROXY -u ALL_PROXY -u http_proxy -u https_proxy -u all_proxy \
  RUSTUP_DIST_SERVER=https://rsproxy.cn \
  RUSTUP_UPDATE_ROOT=https://rsproxy.cn/rustup \
  bash -lc 'curl --proto "=https" --tlsv1.2 -sSf https://rsproxy.cn/rustup-init.sh | sh -s -- -y'
source "$HOME/.cargo/env"
```

## 推荐 `.cargo/config.toml`

```toml
[source.crates-io]
replace-with = "rsproxy-sparse"

[source.rsproxy-sparse]
registry = "sparse+https://rsproxy.cn/index/"

[registries.rsproxy-sparse]
index = "sparse+https://rsproxy.cn/index/"

[net]
git-fetch-with-cli = true
```

## 最小验证

```bash
env -u HTTP_PROXY -u HTTPS_PROXY -u ALL_PROXY -u http_proxy -u https_proxy -u all_proxy \
  curl --max-time 30 https://rsproxy.cn/index/config.json
env -u HTTP_PROXY -u HTTPS_PROXY -u ALL_PROXY -u http_proxy -u https_proxy -u all_proxy \
  curl --max-time 30 https://rsproxy.cn/rustup-init.sh | head
rustup --version
rustc --version
cargo --version
```

## 回归

```bash
bun run rust:preflight
bun run cargo:check:probe
```
