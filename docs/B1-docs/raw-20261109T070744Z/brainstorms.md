---
raw_id: raw-20261109T070744Z
status: brainstormed
created_at: 2026-11-09
---

# Brainstorms

## 覆盖域

- `docs/system/workspace/scripts/quality/governance-merge-gate`：`issue_paths` 的构造、GATE 1（timestamp 一致性）、以及后续把 issue_paths 当 owner 的 phase-vs-code / review-artifact / milestone 校验。
- `bin/governance-merge-gate`、`.githooks/pre-merge-commit`、`docs/system/workspace/hooks/pre-merge-commit.sh`：门禁的执行入口（确认是 `--staged` 还是 `--range`）。
- `pr-merge-guarded` 的 merge 流程：确认它在主仓 develop 上 `git merge`，由 pre-merge-commit hook 触发门禁。

## 决策 1：问题定义是「死锁」，不是「门禁太严」

GATE 1 的意图是防止一个工位顺手改别人的治理状态。这个意图必须保留。真正的问题是：**一份历史损坏的文档没有任何可读的生命周期状态**，因此「修它的结构」与「改它的治理状态」在门禁看来无法区分，导致修复动作永远被拒。

## 决策 2：判定标准选「基线副本不可解析」

三种候选判定：

| 判定 | 评价 |
|---|---|
| 按 diff 内容判断（只改了 frontmatter 行） | 需要精确的语义 diff，实现复杂且易被构造绕过 |
| 按路径白名单（豁免清单文件） | 需要额外维护一份清单，且清单本身要过门禁 → 又一个死锁 |
| **基线副本不可解析** | 语义最贴近：不可解析 ⇒ 生命周期从未读到过它 ⇒ 修结构不改变治理状态 |

选第三种。它不需要任何人工清单，也无法被「顺手改别人状态」利用（基线能解析就照常报错）。

## 决策 3：必须覆盖 `--staged` 路径

`pr-merge-guarded` 的 merge 在主仓 develop 上执行，由 `pre-merge-commit` hook 触发，门禁走 `--staged`（`git diff --cached`）。如果豁免只在 `--range` 模式生效，死锁依然存在。所以 `baseline_text` 在 staged 模式下取 `HEAD`（即合并前的 develop）。

## 决策 4：不依赖尚未合并的解析器

`parse_issue_text`（#4148）来自另一个分支。门禁必须先于它进入 develop，所以判定用**纯 YAML** 实现：glued 闭合、成对冲突标记、YAML 解析失败三类都判损坏。legacy bullet-only 文档（无 `---` 块）是受支持格式，不判损坏。

## 决策 5：剔除而不是逐条降级

初版做法是把 GATE 1 的 mismatch 降级为 warning。实测发现后续还有 phase-vs-code、review-artifact、milestone 归属三类校验会继续报错（共 28 条）。正确做法是把这类路径**整体从 owner 集合剔除**：它们本来就不属于本次 merge 的 owner。

## 被否决

- 直接 `--no-verify` / `FREELY_SKIP_IBM_GATE`：前者跳过门禁，后者对含代码的 merge 会拒绝，且都需要违规理由。
- 用安装版（`~/.freely/versions/*`）覆盖门禁：merge hook 用 `git rev-parse --show-toplevel` 取主仓脚本，安装态不参与。
- 把 23 份修复拆成 23 个工位：违反「一次性存量修复」的 issue 要求，且每个工位仍需先过 GATE 1。
- 只修 `--range` 不改 `--staged`：PR 合并仍会被挡，等于没修。
