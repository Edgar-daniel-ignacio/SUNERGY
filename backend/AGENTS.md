# Backend scope
Read root AGENTS.md and relevant routing documents first.

`sunergy.api` is transport only; application functions must be callable without
HTTP. `contracts` owns external Pydantic shapes. Physics uses ordinary typed
structures and never imports Dash, plotting, browser state, or legacy modules.
Boundary validation is not scientific verification. No runtime network/file work
at import. Configuration loading is explicit; every write uses an isolated path.
Keep tests offline. A placeholder must raise/return a clearly unavailable state,
never synthetic production results. Regenerate OpenAPI after contract edits.
