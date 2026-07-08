# Tasks: scan platform detection
- issue_id: I-20260708T222454Z-A

## 1. _sync_platform_direct 重构
- [ ] 添加 phase_state 参数
- [ ] 先 update_issue(body=phase_state)
- [ ] 逐平台 fetch_issue_state
- [ ] 只 close OPEN 的平台
- [ ] 调用点传入 phase

## 2. platform-only 检测
- [ ] 遍历 platform_issues (所有平台 OPEN issues)
- [ ] 提取 raw_key
- [ ] 比对 seen_keys → 未出现的加入 items
- [ ] 生成正确的 next_action

## 3. 逐平台状态比对
- [ ] 用 fetch_issue_state 替代 all_platform_states.get(gh_id)
- [ ] 遍历 configured_platforms
- [ ] platform_mismatches dict 记录每个平台的差异

## 4. 测试验证
- [ ] 创建 test issue (#3835) 双平台
- [ ] 场景A: GitHub CLOSED + Gitee OPEN → scan 检测
- [ ] 场景B: 两个都 OPEN + local terminal → scan 同步
- [ ] AT-001/002/003 全部 PASS
