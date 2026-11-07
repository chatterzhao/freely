# Brainstorms: raw-20261103T132526Z

## 问题

平台写通道在失败时**自证成功**，两条独立缺陷叠加：

1. **调用契约失配**：`bin/issue-sync` 用「方法名 + JSON 串」位置参数调 `gitee-issue.py`，被调侧 argparse 只接受「子命令 + 具名 flag」→ 每次调用退出码 2；外层 `|| echo '{"ok":false}'` 把它变成「合法 JSON 空结果」。
2. **门禁变量从未赋值**：`grep GITEE_TOKEN bin/issue-sync` 只有 4 处条件判断、无任何赋值；凭证权威来源是 `gitee-issue.py` 的 `freely_user_env`。按文档把 token 放文件 → `-n "${GITEE_TOKEN:-}"` 恒假 → **整段 Gitee 写操作被静默跳过**，脚本继续写 `platform_state open` 并打印 `create complete`。
3. **探测四因合一**：`platform-adapter.py` 的 `GitHubHandler.detect()` 把「未安装 / 未认证 / 超时 / 无仓库权限」压成一个 `False`，`create_issue()` 再翻译成 `unsupported platform: github` —— 真实故障被误导成「平台不支持」。
4. **部分成功被抹成整体失败**：`create-issue` 只有全部 created 才 `exit 0`，否则 `exit 1`；`freely cmd_feedback` 又用文本 grep 判状态，`status` 落到 pretty-print 第 3 行即漏判。结果是「已创建但命令报失败」，按退出码重试就造重复 issue。

## 证据（本机实测）

- `bin/issue-sync:_gitee_repo` 的 awk 对 `git@gitee-zhaoquan:zhaoquan/freely.git` 产出 `git@gitee-zhaoquan:zhaoquan/freely`（带 host 段、未剥 `.git`）；重构后实测为 `zhaoquan/freely`。
- 基线快照（`git archive HEAD`）跑 AT-001：**15 项失败**，其中 `gitee create` 直接因契约失配失败、`repo url` 三条全错、`partial create` 退出码 1、`unsupported platform` 仍出现。
- 真实仓库只读核验：`_gitee_repo` → `zhaoquan/freely`；adapter 探测 `Available: ['github', 'gitee']`，两平台 repo 均正确。

## 证伪（未被现有 open issue 覆盖的部分）

- #4184 是「`issue-sync close` 在非终态时先关平台再报错」，属**关闭路径**的部分成功；本 issue 只修**写原语与创建路径**，关闭路径的部分口径在 `cmd_close` 里显式标注归 #4184，不夹带。
- #4154 是契约常量与 raw key 多副本收口；本 issue 只把 gitee 调用契约对齐到 adapter 已在用的形态（`gitee-issue.py --repo X <sub> --flag`），不做常量收口。
- #4150（已合并）是读通道 verdict；#4195（已合并）是读通道降级标记。写通道此前无人覆盖。

## 关键设计

1. **写原语换成真契约**：`_gitee_cli <action> [flags]` 包住 `gitee-issue.py`，失败**原样返回非零**，不再有 `|| echo` 兜底；`_gitee_create/_gitee_update/_gitee_comment/_gitee_close` 四个薄封装。
2. **token 权威单点**：删掉 bash 侧 `GITEE_TOKEN` 判断，token 只由 `gitee-issue.py` 的 `freely_user_env` 读取。
3. **仓库身份可测**：抽出纯函数 `_gitee_repo_from_url`，覆盖 scp-like / ssh / https 三种形态。
4. **先拿 id 再写状态**：`platform_state` 是对**所有**已配置平台的断言；任一平台失败即不写，退出码 3（部分成功），已创建平台的 id 已落 frontmatter，重跑可自愈。
5. **探测报因**：`detect_reason()` 返回 `(ok, reason)`，四类原因分别可读；`_unavailable_error()` 把「unavailable: gh not installed (gh: command not found)」写进结果，取代 `unsupported platform`。
6. **按平台记账**：`create-issue` 退出码 0 / 3 / 1；`freely cmd_feedback` 改为 JSON 解析并按平台逐条汇报。

## 被否决的替代方案

- 给 `_gitee_call` 加一层 JSON→flag 转换（保留旧签名）：多一层易错的字符串拼装，直接换薄封装更干净。
- 在 bash 侧读 token 再传给 gitee-issue.py（两处权威）。
- 继续用文本 grep 判状态（`json.dumps(indent=2)` 下 status 行位置不稳定）。
- 把关闭路径的部分成功一并修（#4184 的 scope）。
- 引入新平台抽象层（超出本 issue，属于 #4166 双平台入口收口）。
