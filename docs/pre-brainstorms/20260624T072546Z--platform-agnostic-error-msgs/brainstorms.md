# Brainstorms: 治理文档平台硬编码修复

## Discovery
wt-create、hook、freely feedback --help 中硬编码 "GitHub"/"gh issue create"/"--repo --title --body"。Freely 多平台设计，报错不应假定平台。

## Research
**根因**：最初只支持 GitHub，报错直接写了 GitHub。后加 Gitee 但报错未跟进。
**方案**：用户可见报错去平台名和参数格式，统一指 `./bin/freely feedback --help`。

## Decision
Promote。纯文案修整。
