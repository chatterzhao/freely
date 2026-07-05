# Brainstorm: issue-sync frontmatter 脏文件根因

## 问题
batch sync 后 199 个 issue.md 变成 dirty。三个独立根因：
1. updated_at 无条件刷新 (168 files)
2. PyYAML datetime 解析 + dump 格式破坏 (~23 files) 
3. created_at 被填为 sync 时间 (~7 files)

## 方案
1. _update_platform_ids: 仅 platform_id 变化时写 updated_at
2. 全局禁用 PyYAML timestamp 自动解析
3. created_at 缺失时从 raw key 时间戳推断

## 决策: promote
