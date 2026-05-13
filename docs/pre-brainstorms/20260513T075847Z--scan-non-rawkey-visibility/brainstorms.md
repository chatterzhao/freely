# Brainstorm: scan non-raw-key platform issue visibility

scan_classification and scan_platform_issues only match open GitHub/Gitee
issues with raw-{key} pattern in title/body. 33 of 66 open issues are
silently dropped from scan output.

Fix: emit platform_only items with gh-{number} key as fallback.
