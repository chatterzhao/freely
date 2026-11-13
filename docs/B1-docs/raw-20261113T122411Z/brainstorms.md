# B1 Brainstorm — raw-20261113T122411Z

## 1. 现象

R33.15（#4343，已合并 `f1be6b5c3`）新增 `wt-close` Phase 2.5 收口所有 I-* children 后，真机收口 R33.15 工位时：

    wt-close: closing I-* issue: I-20261113T115957Z-A
    Error: no platform_ids for I-20261113T115957Z-A
    Error: platform close failed for I-20261113T115957Z-A; cleanup stopped

但该 I-* 的 `platform_ids` 是齐全的（github 4344 / gitee IKV7KY）。

## 2. 根因（已复现）

Phase 2.5 用 TSV 在 python → bash 传 children 报告：

    print("%s\t%s\t%s\t%s" % (child, phase_state, platform_state, path))

bash 用 `while IFS=$'\t' read -r cid phase platform_state path` 解析。

当 `platform_state` 为空（`promote-finalize` 后 linked 文档的默认形状）时，输出为 `child\tcompleted\t\t/path`。bash 的 IFS 把 tab 视为**空白字符**，连续分隔符被折叠：

- `platform_state` = `/path`
- `path` = 空

于是 `_close_platform_ids_readonly "" "$cid"` → `_fm_get ""` 读不到文件 → 空 → `no platform_ids`。

AT 的 fixture 当时都给了非空 `platform_state`，所以未覆盖真实形状。

## 3. 方案

| 方案 | 做法 | 评价 |
|---|---|---|
| A | 空字段输出占位符 `-`，bash 侧把 `-` 当作空 | 最小、TSV 列永不空、可读 ✅ |
| B | 改用非空白分隔符 `\x1f`（US） | 更彻底，但 bash 侧 `IFS=$'\x1f'` 可移植性稍差（macOS bash 3.2 支持） |
| C | 用 JSON 传递整份报告 | 需要 python 解析，改动大 |

采用 A：python 里 `or "-"`，bash 侧对 `-` 的处理与空等价（`!= closed` 即视为未关；phase `-` 走非终态分支拒绝）。

## 4. 证伪

- 「是 platform_ids 真的缺失」→ 否：直接解析文档得到 4344 / IKV7KY。
- 「是 _fm_get 坏了」→ 否：单独调用 `_fm_get <file> platform_ids` 正常输出 JSON。
- 「是路径匹配错」→ 否：glob 单独跑返回正确绝对路径；错的是**列解析**。

## 5. 测试要点

- 新增用例：两个 child 的 `platform_state` 都为空 → 仍关闭 2 次（修复前必红）。
- 基线（develop）同用例：报告列错位 → 报 `no platform_ids`/零调用 → 红。
