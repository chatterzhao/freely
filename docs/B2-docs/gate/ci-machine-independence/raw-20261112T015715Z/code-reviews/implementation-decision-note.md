# Implementation Decision Note
- issue_id: I-20261112T015715Z-A
- issue_path: docs/B2-docs/gate/ci-machine-independence/raw-20261112T015715Z/issues/I-20261112T015715Z-A.md
- decision: 只在 `test-contract-single-source.py::registry_checks` 内自建 tempfile cline stub、用 `dict(os.environ)` 拷贝注入三个 `subprocess.run(..., env=env)`；新增 AT-001（10 静态 + 3 行为含负向控制）进 `CORE`/`CI_CORE`；注册 `gate/ci-machine-independence` story。不改任何产品脚本。
- why_this: 产品侧「只部署 `command -v` 找得到的工具」是正确的，错的是测试把「本机装了 cline」当成未声明前提。把环境前提收进测试进程内部后，断言真正验证 registry 被读取，CI 结果与机器无关，`test-gate` 证据重新可移植，且改动面最小。
- alternatives_considered: ①临时改全局 `os.environ["PATH"]` 再改回——异常时会泄漏、作用域脏，否决；②stub 放进沙箱 `tree/bin/`——`command -v` 只看 PATH，行不通，否决；③改用显式 `--tools` 绕开 registry——等于删掉被测能力，否决；④CI 预装 cline / 全局 shim 制度化——换台机器仍红，且要求所有贡献者装 cline，否决；⑤把该项移出 CI_CORE 或标 known-broken——削弱验收面、掩盖真实漂移，否决；⑥B1 Option B 重做 deploy-skills 可观测性——改动扩散到产品代码，超出本 fix scope，列为后续。
- boundary_non_goals: 不改 `bin/deploy-skills`、`bin/test-all` 的既有成员、`test-gate`、任何门禁、`.size-budget`、`projection.lock`；不改 registry 内容；不改 `CI_CORE` 成员集合（只增 AT）；不把 R33 的人工 shim 变成制度。
- residual_risk: ①stub 名与 registry 的 `cline.test_command` 首词绑定，将来改名需同步（AT 静态 S3 + candidate revisit_trigger 守着）；②stub 只让 `command -v` 成立、不模拟 CLI 行为，若将来断言开始执行 cline 需换真 mock；③若 `deploy-skills` 更换 installed 判据，stub 会失效，AT 负向控制会暴露；④`docs/epics-map.svg` 手工增条目时须保留原有底色排版，否则视觉回归（R33 踩过）。

## 为什么负向控制不可省

stub 让 `cline` 必然出现在 `--dry-run` 输出，若只加 stub 不加控制，断言可能变成永真。
AT-001 的 B3 把沙箱 registry 的 `cline.test_command` 首词改成绝不存在的二进制名，
期望 `registry present` 判红 —— 这证明输出里的 cline 来自 registry 读取链路，
而不是被 stub 名硬编码绕过。这是「修测试」与「放松测试」的分界线。
