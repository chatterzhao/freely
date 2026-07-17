# 历史状态收敛证据包（供 batch-reconcile 合规通道执行）

- 生成: 2026-07-17，raw-20260715T121608Z lane（承载 raw-20260715T122119Z）
- 阻塞原因: GATE 1 跨 raw 工位隔离（实拦记录见 code-reviews/IDN），单工位不得批改他 key 文件
- 后续通道: raw-20260717T*（batch-reconcile 能力缺口立案）落地后执行，或逐 key 工位

## A. 3 个 I-* → completed（merge 实证，无 gate 欠账）
| I-* | 现值 | merge 实证 |
|---|---|---|
| I-20260612T000223Z-A | done_b2_ibm | 7e1057dc2 |
| I-20260616T030213Z-A | done_b2_ibm | b4e6d5d99 (Merge fix/raw-20260616T030213Z-b1) |
| I-20260615T001626Z-A | in_b2_ibm | 4f5183b71 (Merge feature/raw-20260615T001626Z-a2a-no-fallback) |

## B. 13 个 legacy raw → absorbed + absorbed_into 锚（平台已全 CLOSED，gh api 实测 2026-07-17）
20260506T100000Z(gh#231) 20260517T113021Z(#521) 113514Z(#522) 113807Z(#523) 114147Z(#524) 114702Z(#525) 115113Z(#526) 115824Z(#527) 120124Z(#528) 120752Z(#529) 121432Z(#530) 20260527T004453Z(PR#2243 MERGED) 20260617T035314Z(#2883)

## C. 6 项不予收敛（显式留档）
- 无 merge 证据: I-20260503T0915Z、I-20260505T1210Z-A-B、I-20260505T1210Z-A-C
- 有实证但 RED-GREEN/tasks 历史欠账（pretests-gate 实拦）: I-20260705T231534Z-A、I-20260706T023422Z-A、I-20260710T171329Z-A

## D. 附带欠账
- C-20260612T000223Z-A promoted 但 milestones 无 candidate_issues 条目（governance gate 实报）
