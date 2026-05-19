# Pre-Tests: task-lifecycle-scan 批量化

> I-20260513T040512Z-A | M-20260513T040512Z-A

## 场景 1: 正常批量化扫描

**前置**: gh CLI 可用，repo 有 50+ issues
**操作**: 执行 `task-lifecycle-scan.py`（含新 Phase 0-3）
**预期**:
- 扫描完成 < 5s
- Phase 0 产生 `platform_all` dict
- Phase 1 输出分类清单（一致/不一致/仅本地）
- Phase 2 输出 `platform_only` 列表（若有）
- Phase 3 输出 chain trace（格式与之前一致）
- 全程仅 1 次 `gh issue list` API 调用

## 场景 2: gh CLI 不可用

**前置**: gh CLI 未安装或 token 过期
**操作**: 执行扫描
**预期**: 
- fallback 到逐项 `gh issue view N`
- 输出 fallback 警告
- 不崩溃

## 场景 3: 无 platform_only issue

**前置**: 本地已包含所有 platform issue
**操作**: 执行扫描
**预期**: Phase 2 输出为空列表

## 场景 4: SKIP_PLATFORM_CHECK 已移除

**前置**: 代码中无 `SKIP_PLATFORM_CHECK` 引用
**操作**: grep 检查
**预期**: 无匹配

## 场景 5: 输出格式兼容性

**前置**: 有已有的 chain trace 输出
**操作**: 对比新旧输出格式
**预期**: Phase 3 输出格式字段与之前一致（仅数据来源从 API 改为本地缓存）
