# 008 — Make evidence review tags selective

## Scope and authorization

The user explicitly requests stricter tagging criteria, cleanup of redundant tags
and an update to the existing PR. Update the tagging rule in root AGENTS and the
affected maintained docs; do not edit PLANS or scoped instructions. Significant
deviations from prior evidence need review, not every agent-edited line. Removing
an unnecessary marker is not human approval of a scientific claim.

Start: `4244a91e8ffc4be3b7c5bbc4c5059553db170e11` on the existing
`docs/legacy-refactorizacion` branch, PR1. Compare the audit against its parent
`7d93b30` to classify actual semantic corrections instead of repeating the audit.
Preserve all evidence wording, source/fixture bytes, identifiers and unrelated
local skill/plan changes. Existing 45-file preservation manifest remains available
at ignored `.local/audit007/preexisting_work.json`.

## Method and ownership

- Lead: root policy, seven canonical/catalogue docs, integration and verification.
- `tag_cleanup_early`: original README and chapters00–06 only.
- `tag_cleanup_late`: chapters07–11 and original four Mermaid files only.
- Use the prior/current diff to identify significant behavior, equation/unit,
  contract, provenance/validity or assumption changes. Remove markers from unchanged
  facts, routine confirmations, rewording, formatting and routing/metadata.
- Group adjacent changes sharing one rationale under one precise scoped note.
  Summary links do not duplicate markers on the owning detailed entry. Remove
  blanket frontmatter review tags; retain the six purpose/routing fields.
- No new physics, acceptance changes, source investigation or capture generation.
  Existing independent numerical evidence and unresolved scientific concerns stay.

## Verification and completion

Check pre/post marker counts, each retained scope/reason, preservation of body text
apart from markers/short review notes, frontmatter/links/Mermaid fences and immutable
evidence/unrelated files. Run repository integrity and diff checks. This docs-only
change does not require re-running numerical/frontend suites locally. Commit only
the cleanup/policy/task record, push the same branch and update PR1 description.
Observe CI; merge still requires the existing human approval and is not part of
this cleanup.

## Results

- Compared original/audited versions before selecting markers. Canonical AN-01's
  algebra and IN-01's preset/manual distinction already existed before the audit,
  so their canonical markers were unnecessary. Significant changes in the authored
  legacy chapters remain locally marked; summaries link to their owning records.
- Retained scopes cover actual changes to weather/POA contracts, effective versus
  reported temperature, method/origin and fit provenance, catalogue reference
  temperature, failure preconditions, statistical/report identity and scientific
  authority. Related adjacent corrections share scoped notes rather than per-cell
  markers. No numerical/evidence statements were removed to meet a tag quota.
- Review markers in body text/diagram comments decreased from 466 to 82 across
  20 maintained Markdown files and four Mermaid files. Removed 20 blanket metadata
  flags. Literal occurrences are 487 to 83 because the catalogue contains one
  explanatory inline-code example; that example is not a pending review marker.
- `.venv/Scripts/python.exe .local/audit008/check_context.py` — all 20 six-field
  frontmatters, 118 local links/anchors, six Mermaid fences and 45 pre-existing
  unrelated file hashes passed. The six purpose/routing fields are unchanged.
- `.venv/Scripts/python.exe .local/audit008/check_preservation.py` — all previous
  evidence words remain in order after removing tags/metadata; only brief scoped
  review notes and the catalogue's authorized policy explanation are added/changed.
  Every noncomment diagram statement is unchanged. This is a temporary cleanup
  check, not a new product/development prerequisite.
- `uv run --locked --offline python scripts/check_repository.py` — configuration,
  preserved evidence/source hashes and import boundaries pass. Scoped
  `git diff --check` passes. Runtime code, contracts, snapshots, fixtures, source,
  scoped instructions and PLANS remain unchanged.
- Canonical tagging received independent read-only review; the IN-01 marker was
  removed as a result. A final curated scan also removed D-05's unchanged
  recommendation marker. Both delegated units verified their evidence preservation.
- Keep PR1 as the sole review path, with the original branch and required human
  approval unchanged. Provider checks own the current CI status after the push.
