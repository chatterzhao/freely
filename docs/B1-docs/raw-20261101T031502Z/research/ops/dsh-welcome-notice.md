# DSH 预览版弹窗“暂时无法保存确认状态”排查记录

日期：2026-11-01
环境：macOS，`dsh 0.2.1-rc.5`（pnpm global），profile `superagent`

## 症状

打开 DSH Web / Superagent 页面出现“预览版说明”弹窗，点“继续”提示：

> 暂时无法保存确认状态，请重试。

弹窗无法关闭，但应用主体可用。

## 根因

DSH 把欢迎声明确认状态存在 profile 的 `cordis.patch.yml`：

```yaml
- id: ui-settings-general
  name: "@deepseek-ai/dsh-client-ui-settings-general"
  config:
    welcomeNoticeVersion: 2026-09-28.1
```

`welcomeNoticeVersion` 是 **volatile** 字段。`config-editor.edit()` 写回后会重新 compose 配置做 read-back 校验；volatile 字段在 compose 时被剥离/重包，导致“写入值 ≠ 回读值”，被判定为 “overridden by home patch / command-line overlay”，设置层拒绝，UI 显示保存失败。

官方仓库没有 issue tracker（`has_issues=false`），同类问题在 Discussions：

- #7959 `config-editor edit() read-back validation permanently fails for entries with volatile fields`
- #9001 `Preview Notice acknowledgement never persists without a DeepSeek account`
- #9155 `Preview Notice cannot be dismissed for non-admin users when host-config writes are denied`
- #7469 `Welcome notice modal permanently locks the UI when settings write fails`
- #7634 `Orphaned profile writer lock silently drops the legacy settings.yaml migration`
- #5523 `Settings persistence follows the page hostname... re-sees welcome notice`

本次最吻合 #7959：不是权限/锁/安装冲突，而是 **已有 volatile block 的 read-back 校验失败**。

## 有效修复（本次已验证）

1. 备份 profile patch：
   ```bash
   cp ~/.dsh/profiles/superagent/cordis.patch.yml \
      ~/.dsh/profiles/superagent/cordis.patch.yml.bak-$(date +%Y%m%d-%H%M%S)
   ```
2. 移除 `- id: ui-settings-general` 整段（只删这一段，保留 `dsh-superagent`/`webserver`/`ui-chat`/`ui-theme`）。
3. 只保留一个实例，重启：
   ```bash
   kill -TERM <old-pid>
   nohup dsh --profile superagent > /tmp/dsh-superagent-restart.log 2>&1 &
   ```
4. 打开新会话，弹窗点“继续”一次；本次弹窗正常关闭。
5. 校验 DSH 已写回：
   ```bash
   grep -A3 'ui-settings-general' ~/.dsh/profiles/superagent/cordis.patch.yml
   ```
   本次 2026-11-01 03:52 写回 `welcomeNoticeVersion: 2026-09-28.1`。

## 不要做

- 不要因为弹窗去重装/编译 DSH；`dsh` 是 pnpm global `0.2.1-rc.5`，与源码 clone 无关。
- 不要同时保留 npm global 的源码 link 和 pnpm global；本次已 `npm uninstall -g @deepseek-ai/dsh`，只留 pnpm。
- 不要同时跑多个 `dsh-tui`/web 实例；会放大锁/状态竞争（本次见两个 `dsh-tui` 高 CPU）。
- 不要删 `~/.dsh/settings.yaml.imported`；它只是旧设置迁移备份。

## 判断顺序（下次）

1. `dsh --version` / `which dsh`：确认只有一个安装。
2. `grep -A3 ui-settings-general ~/.dsh/profiles/<profile>/cordis.patch.yml`：是否已有 volatile block。
3. 有 → 备份、删 block、重启单实例、新会话点继续。
4. 无但还失败 → 查 `settings/describe` 是否缺 `ui-settings-general`、profile writer lock、home patch/CLI overlay。
5. 仍失败 → 提 Discussions（官方无 issues），附版本/profile/`settings/describe`/日志。

## 2026-11-01 复发与永久修复

现象：移除 block、重启、点“继续”后弹窗关闭；但 DSH 把 `welcomeNoticeVersion` 写回 profile patch，下一次启动又出现同样的“暂时无法保存确认状态”。

结论：**删 block 只是一次性绕过**。只要已有 `ui-settings-general` 的 volatile block，`config-editor.edit()` 的 compose read-back 就又会失败。

按官方 #7959 的建议做 document-faithful read-back：

- 文件：
  `~/Library/pnpm/global/v11/05005a99cef1205815f96623dea15603c939a0254347f3a04ff5a027501b500d/node_modules/.pnpm/@deepseek-ai+dsh-config-editor@0.2.1-rc.5_33bfdbb9f88875707e13cfc2bc9d2f4c/node_modules/@deepseek-ai/dsh-config-editor/lib/index.js`
- 备份：同目录 `index.js.bak-YYYYMMDD-HHMMSS`
- 把原来的：
  ```js
  flatten(composeEntries([patches])).find(row => row.id === entry.options.id)?.config
  ```
  改成按实际写入的 document 读取：
  ```js
  const persistedRows = yaml.load(String(document), { schema: entryListSchema });
  const persisted = flatten(persistedRows).filter(row => row.id === entry.options.id && row.insert === undefined).at(-1);
  persisted?.config ?? {}
  ```
- `node --check` 通过后，重启单个 `superagent` 实例。

注意：

- 这是 **对已安装包的本地 patch**，DSH 升级/重装会覆盖；升级后要重打，或等官方 fix。
- 不要同时改源码 clone 的同一文件；源码开发用 `pnpm dsh`，与安装版分开。
- 修复后仍需一次“新会话 → 继续”让 write 落盘；之后 profile patch 里应有 `welcomeNoticeVersion: 2026-09-28.1`。

## 2026-11-01 再次复发：先确认进程

补丁生效后仍报同样文案，检查发现 **`:3082` 没有监听、没有任何 `dsh --profile` 进程**。浏览器里的旧页面连的是已死实例，保存必然失败。

先查：

```bash
lsof -nP -iTCP:3082 -sTCP:LISTEN
ps aux | grep '[d]sh .*--profile'
```

没有进程时重启：

```bash
cd <project-root>
nohup dsh --profile superagent > /tmp/dsh-superagent-live.log 2>&1 &
grep 'dsh web' /tmp/dsh-superagent-live.log
```

用日志里的**新 token URL** 打开，而不是刷新旧 tab。旧 token 属于死实例。
