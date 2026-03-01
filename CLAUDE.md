# CLAUDE.md

Static site generator for [static.krcg.org](https://static.krcg.org) — VTES card data, images, and resources. Fetches from VEKN, TWDA, and KRCG rulings.

## Commands

```bash
uv sync --extra dev                          # install (dev)
uv run ruff format --check . && uv run ruff check  # lint
LOCAL_CARDS=1 uv run pytest -vv              # test (needs LOCAL_CARDS=1)
just test                                    # lint + test
LOCAL_CARDS=1 uv run krcg-static build       # full build
LOCAL_CARDS=1 uv run krcg-static build --minimal  # web resources only
just static                                  # build + deploy (both servers)
just minimal                                 # minimal build + deploy (one server)
```

## Architecture

- Single module: `krcg_static/__init__.py` (~630 lines)
- Core dep: `krcg` (>=4.18) — card parsing, TWDA, rulings via `vtes.VTES` / `twda.TWDA`
- `static/` → source assets (committed, includes ~6k card images + symlinks)
- `build/` → generated output (git-ignored), rsync'd to production

Build steps: copy `static/` → zip cards → load VEKN data → generate `build/data/{vtes,twda}.json`, `twd.htm`, `amaranth_ids.json`

Card images: ASCII-only lowercase filenames, crypt cards use symlinks. `CARD_RENAME` dict maps legacy names.

## Testing

`tests/test_static.py`: `test_card()`, `test_twda()`, `test_images()`
`tests/conftest.py`: loads VEKN + TWDA from `tests/twda_test.html` at session start.

## Conventions

- Python 3.12+, ruff (default config)
- `static/` dir including card images and symlinks is committed to git

## Context7 Library IDs

Always use Context7 MCP (`resolve-library-id` + `query-docs`) for docs lookup.

uv: `/astral-sh/uv` | ruff: `/astral-sh/ruff` | pytest: `/pytest-dev/pytest` | just: `/casey/just`
GitHub Actions: `/websites/github_en_actions` | setup-uv: `/astral-sh/setup-uv` | checkout: `/actions/checkout`
