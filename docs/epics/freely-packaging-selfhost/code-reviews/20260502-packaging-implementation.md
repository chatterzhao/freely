# Code Review: Freely 打包与自举验证

- issue_id: I-20260502-0500-A
- review_date: 2026-05-02

## Implementation

- `bin/freely-package`：打包脚本，根据 package-allowlist.txt 复制 workspace 能力文件到版本目录
- `bin/test-pre-merge-selfhost`：自举验证门禁，打包 → 启动 daemon → 验证 Manager cycle
- `docs/system/workspace/package-allowlist.txt`：打包清单，定义 Freely 产品交付内容

## Verification

- 打包版本 `freely doctor` 全部 PASS
- 打包版本成功启动 daemon，完成 Manager cycle，正常停止
