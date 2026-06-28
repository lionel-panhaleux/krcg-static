# CLAUDE.md

Static site generator for [static.krcg.org](https://static.krcg.org) — VTES card data, images, and resources. Fetches from VEKN, TWDA, and KRCG rulings.

## Commands

```bash
uv sync                                      # install (dev group is default)
uv run ruff format --check . && uv run ruff check  # lint
uv run pytest -vv                            # test (offline, packaged krcg data)
just test                                    # lint + test
uv run krcg-static build                     # full build
uv run krcg-static build --minimal           # web resources only
uv run krcg-static build --data              # data files only (cards, TWDA)
just static                                  # build + deploy (both servers)
just minimal                                 # minimal build + deploy (one server)
just data                                    # data-only build + deploy data/ (cron)
```

## Architecture

- Single module: `krcg_static/__init__.py`
- Purpose: regenerate the data files often (cron) so `krcg.load_online` consumers
  track VTES data. **Cards** come from the packaged krcg snapshot (the `fix_csv`
  pipeline is mandatory) → fresh cards need a krcg release. **TWDA** is fetched
  live from source each build, so it stays current without a krcg release.
- Core dep: `krcg` (>=5.0) — card parsing, TWDA, rulings via the v5 API:
  `loader.load_local()` (a `CardDict`) for cards; `twda.fetch_from_source(cards)`
  for a live TWDA (falls back to `twda.load_local()` if unavailable/offline).
  No singletons, no `LOCAL_CARDS`.
- `static/` → source assets (committed, includes ~6k card images + symlinks)
- `build/` → generated output (git-ignored), rsync'd to production

Build steps: copy `static/` → zip cards → `loader.load_local()` + `load_twda()`
→ serialize (`msgspec.to_builtins`) **only the v5** files into `build/data/v5/`
(`vtes.json`, `expansions.json`, `twda.json`). `--data` skips the image copy/zip
and refreshes only `build/data/` (for the frequent cron; `just data` rsyncs just
`data/`).

### Data versioning (`build/data/`)

- `v5/` — the only **generated** data; the layout `krcg.load_online` expects.
- `v4/` — a **frozen committed snapshot** under `static/data/v4/`, shipped as-is
  (no per-build regen): `vtes.json` / `twda.json` (built once with `krcg==4.19`,
  the v4 API being gone from krcg ≥5), plus `twd.htm` / `amaranth_ids.json`.
- root `data/{vtes,twda,twd.htm,amaranth_ids}` are committed symlinks → `v4/*`
  (retrocompat now; flip to `v5` in a couple of months).
- `standard_html` and `amaranth_ids` stay as **manual utilities** to refresh the
  frozen snapshot offline; the build no longer calls them.

Card images: ASCII-only lowercase filenames from the card name as printed; crypt
cards keep group-less (and `…adv`) symlinks. v5 names the article naturally
("The Ankou" → `theankou`); legacy v4 back-form files (`ankouthe`) remain and the
natural names symlink onto them. `CARD_RENAME` maps vtes.pl downloads to the
committed names.

## Testing

`tests/test_static.py`: `test_card()`, `test_twda()`, `test_images()`.
`tests/conftest.py`: session-scoped `cards` / `TWDA` fixtures via `loader.load_local()`
and `twda.load_local()` (offline, from the packaged krcg snapshot).

## Conventions

- Python 3.12+, ruff (default config)
- `static/` dir including card images and symlinks is committed to git

## Context7 Library IDs

Always use Context7 MCP (`resolve-library-id` + `query-docs`) for docs lookup.

uv: `/astral-sh/uv` | ruff: `/astral-sh/ruff` | pytest: `/pytest-dev/pytest` | just: `/casey/just`
GitHub Actions: `/websites/github_en_actions` | setup-uv: `/astral-sh/setup-uv` | checkout: `/actions/checkout`
