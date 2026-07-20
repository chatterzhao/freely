---
local_id: raw-20260616T110714Z
kind: raw
phase_state: absorbed
absorbed_into: I-20260616T110714Z-parse-env-removal
platform_ids:
  github:
    issue_id: '2842'
    url: https://github.com/chatterzhao/freely/issues/2842
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-06-16T11:07:31Z'
updated_at: '2026-07-18T02:07:56Z'
intake_id: ''
author: platform
channel: github
session_refs: []
---

## 问题

`freely_config.py` 的 `cmd_init_toml` 在第143行调用 `parse_env_file(env_path)`，但该函数在 commit `a899aeb3` 中被移除后，commit `5cc06494` 只恢复了调用却没有恢复函数定义。

```python
def cmd_init_toml(args: argparse.Namespace) -> None:
    data: dict[str, Any] = {}
    if args.from_env:
        env_path = Path(args.project) / ".freely" / "config.env"
        if env_path.is_file():
            data = parse_env_file(env_path)  # ← NameError: name 'parse_env_file' is not defined
```

## 影响面

- `freely_config.py init-toml --from-env` 直接崩溃
- `load_config()` 中的自动迁移路径完全失效（stderr 被 `2>/dev/null` 吞掉）
- 老项目每次启动回退到 `source config.env`，永远不会完成迁移到 TOML

## 验证

```bash
python3 -c "import freely_config; print('parse_env_file' in dir(freely_config))"
# 输出: False
```

## 修复方向

恢复 `parse_env_file` 函数定义（在 `read_config` reader 区域），并增加类型推断：
- `"true"/"false"` → bool
- 纯数字 → int/float

同时修改 load_config 不要吞掉 stderr，让迁移失败可见。
