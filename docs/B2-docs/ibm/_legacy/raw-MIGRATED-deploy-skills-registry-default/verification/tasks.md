# Tasks: deploy-skills 默认部署到全部已安装 tool

- issue_id: I-20260624T004510Z-A

## T1: 修复 opencode 通配符 ✅
- file: bin/deploy-skills:99
- change: `opencode)` → `opencode*)`
- status: done

## T2: 默认 tool 从 registry 驱动 ✅
- file: bin/deploy-skills:69-91
- change: 替换旧 fallback 链为 registry 驱动的自动检测
- status: done

## T3: 更新 usage 文档 ✅
- file: bin/deploy-skills:7-33
- change: 反映新的默认行为和 opencode* 支持
- status: done

## T4: 手动测试验证 ✅
- test: --dry-run 默认、openocode-apikey-*、--tools 显式
- status: done

## T5: B1/B2 治理文档 ✅
- brainstorms.md, candidates.md, milestones.md
- I-issue, PRD, pre-tests, code-review
- status: done
