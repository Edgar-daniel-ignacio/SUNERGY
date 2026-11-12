# 006 — Install the requested marimo-notebook skill

## Scope and starting state

Install `marimo-team/skills` at `skills/marimo-notebook` using the existing
uvx/deno skills CLI format: project `.agents/skills/`, Claude junction and root
`skills-lock.json`. No notebook creation, runtime dependency change, skill rewrite,
commit/staging, or changes to other installed skills.

Current branch is `codex/backend-reproduction-foundation`. Preserve all existing
refactoring/simplifier modifications and untracked plan/skill files. Read root
guidance, planning protocol, installed skill-installer guidance, current lockfile
and tracked skill/junction layout. Exact upstream SKILL.md retrieved through GitHub.

## Procedure and verification

1. Inspect CLI options and explicit upstream path; confirm destination absent.
2. Install only the named skill for project Codex/Claude using skills CLI.
3. Check upstream identity/content, complete references, junction target and lock
   entry; validate structure and inspect final diff, preserving old lock entries.

## Actual results

- Existing entries are ast-grep, marimo-pair and pydantic; Claude paths are junctions.
- `uvx deno` in the sandbox hit interpreter-cache write restrictions. Using scoped
  approved execution and repository-local UV/Deno caches succeeded.
- `uvx deno -A npm:skills add --help` resolves skills 1.7.6 and confirms explicit
  skill/agent selection. No global install or dependency manifest changes needed.
- Installed successfully with:
  `uvx deno -A npm:skills@1.7.6 add https://github.com/marimo-team/skills/tree/main/skills/marimo-notebook --skill marimo-notebook --agent codex claude-code --yes`.
- Canonical directory contains SKILL.md and 13 supplied reference files. Claude
  path is a junction to it, matching the existing installation layout.
- Root lock records source `marimo-team/skills`, ref `main`, exact skill path and
  computed hash. All three previous lock entries remain semantically unchanged.
- Bundled quick_validate passes. Installed SKILL.md Git blob matches independently
  fetched upstream blob `20bc48f2f8235c7ab206fc5bb31a3ba58d7e8925` after checkout
  newline normalization. All 14 local Markdown links resolve; junction content
  matches canonical bytes. No upstream instructions were applied to production.
- Inspected lock diff and final status; only requested install paths/lock plus this
  plan were added by this task. Existing changes preserved. No notebook/runtime
  execution or application build needed for the upstream skill installation.
- Complete. Installation files remain unstaged, like normal source changes; no
  commit. Skill is available next turn. No reproduction/scientific gate claimed.
