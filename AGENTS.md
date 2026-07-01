# Agent instructions — nano-docs (docs.nano.org)

The Nano developer documentation, built with **MkDocs (Material)**. Live at
**docs.nano.org** (served by GitHub Pages from the built `site/`).

Task tracking is **beads** — run `bd prime` first. Use `bd` for all tasks; do
not create markdown TODO lists.

## Make a change and ship it

- Documentation content is Markdown under **`docs/`**; navigation and theme are
  in `mkdocs.yml`. Edit those, then open a PR.
- Build locally to check: `pip install -r requirements.txt && mkdocs build --strict`.
- Publishing is via the workflows in `.github/workflows/` (mkdocs build →
  published site). Check those files for the exact production trigger; the live
  origin is GitHub Pages serving the generated `site/`.

## Infra

This site is static and not part of the Cloud Run stack, so it has minimal
shared infra. For the overall nano.org topology see the **[shared infra map](https://github.com/nanocurrency/nano-org/blob/main/docs/agents/INFRA.md)**.

## Agent-doc policy — IMPORTANT

Only the built MkDocs `site/` (generated from `docs/`) is published. Keep this
`AGENTS.md` and any agent material at the **repo root** — **never put agent
docs inside `docs/`**, or MkDocs will publish them to docs.nano.org.
