# PRD: raw-20261127T131717Z
## Goal
平台身份只由规范标题前缀决定，正文提及不得制造假歧义。
## 实现方案
platform-adapter 新增 `is_identity_title()`；GitHub 搜索改为 title-only 并过滤；Gitee 候选过滤改用同一函数。
## Dev-Loop Handoff
RED 1/10 → GREEN 11/0；runtime unit 覆盖纯函数与查询路径。
