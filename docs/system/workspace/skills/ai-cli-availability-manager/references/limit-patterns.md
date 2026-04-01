# 限流检测模式

本文档定义各 AI CLI 工具的限流检测正则模式。

## 通用限流模式

所有工具共享的基础模式：
```regex
rate.?limit|429|too.?many.?requests|quota.?exceeded|limit.?reached
```

## 工具特定模式

### codex

```regex
5-hour.*limit|weekly.*limit|rate.?limit|429|token.*limit|concurrent|subscription.?expired|401|unauthorized
```

匹配示例：
- `You've reached your 5-hour limit`
- `Weekly message limit exceeded`
- `Rate limit exceeded. Please retry after 60 seconds`
- `429 Too Many Requests`
- `Your subscription has expired`

### iflow

```regex
rate.?limit|429|quota.?exceeded|limit.?reached|too.?many.?requests|usage.?limit
```

匹配示例：
- `请求频率超限`
- `429: Too Many Requests`
- `Quota exceeded for this billing period`

### kiro

```regex
rate.?limit|429|quota.?exceeded|limit.?reached|monthly request limit reached|unable to verify subscription status:\s*service error
```

匹配示例：
- `Monthly request limit reached`
- `Unable to verify subscription status: service error`

## 认证失败模式

```regex
401|unauthorized|invalid.?token|token.?expired|authentication.?failed|请先登录
```

匹配示例：
- `401 Unauthorized`
- `Invalid authentication token`
- `Token has expired`

## 检测实现

```bash
check_rate_limit() {
  local output="$1"
  local tool="${2:-all}"
  
  local patterns=""
  case "$tool" in
    codex)
      patterns="5-hour.*limit|weekly.*limit|rate.?limit|429|token.*limit|concurrent|subscription.?expired|401|unauthorized"
      ;;
    iflow)
      patterns="rate.?limit|429|quota.?exceeded|limit.?reached|too.?many.?requests|usage.?limit"
      ;;
    all|*)
      patterns="rate.?limit|429|too.?many.?requests|quota.?exceeded|limit.?reached"
      ;;
  esac
  
  if echo "$output" | grep -qiE "$patterns"; then
    return 0  # 检测到限流
  fi
  return 1  # 未检测到限流
}
```

## 冷却时间建议

| 限流类型 | 建议冷却时间 | 处理策略 |
|----------|-------------|----------|
| 5小时限制 | 5小时 | 切换到其他 profile |
| 每日限制 | 24小时 | 切换到其他 profile |
| 分钟级限流 | 1-5分钟 | 等待后重试同一 profile |
| 认证失败 | N/A | 标记 profile 失效，切换 |
