# Tasks: ai-auth Template Config Files

## T1: Create claude-apikey-EXAMPLE
**File**: `templates/ai-auth/claude-apikey-EXAMPLE/settings.json.example`
**Dependencies**: None
**Effort**: Small

## T2: Create codex-account-EXAMPLE
**File**: `templates/ai-auth/codex-account-EXAMPLE/config.toml.example`
**Dependencies**: None
**Effort**: Small

## T3: Create opencode-apikey-EXAMPLE
**File**: `templates/ai-auth/opencode-apikey-EXAMPLE/settings.json.example`
**Dependencies**: None
**Effort**: Small

## T4: Create README.md
**File**: `templates/ai-auth/README.md`
**Dependencies**: T1-T3
**Effort**: Medium

## T5: Create zshrc-aliases.example
**File**: `templates/ai-auth/zshrc-aliases.example`
**Dependencies**: None
**Effort**: Small

## T6: Update freely init
**Target**: `freely init` command
**Dependencies**: T1-T5
**Effort**: Medium

## T7: Update skill references
**Target**: `tool-config-matrix.md`, `auth-setup.md`
**Dependencies**: T1-T5
**Effort**: Small
