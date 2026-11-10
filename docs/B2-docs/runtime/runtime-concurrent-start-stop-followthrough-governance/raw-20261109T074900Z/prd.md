# PRD: pkill -f 项目路径正则转义
- issue_id: I-20261109T074900Z-A
- source_raw: raw-20261109T074900Z
- milestone: M-20261109T074900Z-A

## 问题
`pkill -f` 把未转义的 `${project}` 拼进正则，含元字符的路径会误匹配其它项目进程。

## 目标
1. 单一 `freely_escape_regex()` helper（re.escape + argv 安全形式）。
2. 两处项目路径站点使用转义结果，正则其余部分不变。
3. 真实 pgrep 反向 PoC 证明不再误杀。

## 非目标
派发 CAS、SSE 实例收敛（拆 #4254）、固定 pattern 站点改造、改清理语义。

## 验收
见 verification/pre-tests.md 的 AT-001。
