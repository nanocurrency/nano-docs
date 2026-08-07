# CLAUDE.md — nano-docs (docs.nano.org)

Full instructions are in **[AGENTS.md](./AGENTS.md)** — read it first. Quick
pointers so the right file is obvious:

- **Editing the developer documentation** (the most common task): content is
  Markdown under **`docs/`**; the navigation and theme are in `mkdocs.yml`. Edit
  those, open a PR, merge to `main` → the built site publishes automatically.
  Undo = revert the commit.
- Build locally to check: `pip install -r requirements.txt && mkdocs build --strict`.
- Overall topology → the shared infra map AGENTS.md links.

Heads-up: only the built `site/` (generated from `docs/`) is published — **never
put agent docs inside `docs/`** (see AGENTS.md, "agent-doc policy").

Task tracking is **beads** — run `bd prime` first.
