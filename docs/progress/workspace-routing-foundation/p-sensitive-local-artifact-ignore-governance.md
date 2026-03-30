# Progress: sensitive-local-artifact-ignore-governance

- issue_id: `I-20260329-2155-A`
- issue_path: `docs/epics/workspace-routing-foundation/sensitive-local-artifact-ignore-governance/issues/sensitive-local-artifact-ignore-governance.md`
- phase_state: `in_dev`
- summary: `develop` 根目录出现过真实 `auth.json`，暴露出仓库对本地敏感副产物缺少最低 ignore 保护。当前批次把这条线 materialize 成独立 issue，准备通过保守 `.gitignore` 规则和 focused `git check-ignore --no-index` regression 锁住最小 contract。
- next_action: 落最小 ignore 规则并通过 focused regression 与 governance-check，避免把未来夹具需求和账号存储架构混入本 issue。
- revisit_trigger: 如果新规则遮住真实 fixture，或后续又复现新的敏感本地文件家族，再回到 IBM 收紧/扩展 ignore contract。
- current_focus:
  - 仅保护真实已复现和高共识的敏感本地文件名/扩展名
  - 不让广泛黑名单伤到现有能力目录或后续 fixture 设计
