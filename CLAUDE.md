# CLAUDE.md

This file provides guidance to AI agents when working in this repository.

## Project Overview

**krcg-static** generates the static website [static.krcg.org](https://static.krcg.org), serving card data, images, and resources for VTES (Vampire: The Eternal Struggle) card game developers. It fetches card data from VEKN, the Tournament Winning Deck Archive (TWDA), and KRCG rulings, then builds a deployable static site.

## Commands

```bash
# Install (dev)
uv sync --extra dev

# Lint & format
uv run ruff format --check .       # format check
uv run ruff check                  # lint

# Test (requires internet for VEKN data fetch)
LOCAL_CARDS=1 uv run pytest -vv

# Combined quality + tests
just test

# Build the static site
LOCAL_CARDS=1 uv run krcg-static build

# Build minimal (web resources only, no card images or data generation)
LOCAL_CARDS=1 uv run krcg-static build --minimal

# Deploy to production
just static                        # full build + rsync to both servers
just minimal                       # minimal build + rsync to one server
```

The `LOCAL_CARDS=1` environment variable is required for tests and builds — it tells the `krcg` library to use local card image files instead of fetching them.

## Architecture

- **Single module**: All build logic lives in `krcg_static/__init__.py` (~630 lines)
- **`krcg` library** (>=4.18): Core dependency providing card parsing, TWDA parsing, rulings, and JSON serialization via `vtes.VTES` and `twda.TWDA`
- **`static/`**: Source assets committed to the repo (card images, icons, fonts, JS/CSS, HTML)
- **`build/`**: Generated output (git-ignored) — a complete website tree rsync'd to production

### Build process (`krcg-static build`)

1. Copies `static/` to `build/` (preserving symlinks)
2. Creates `build/card/_all_cards.zip`
3. Loads card data and TWDA from VEKN
4. Generates `build/data/vtes.json`, `build/data/twda.json`, `build/data/twd.htm`, `build/data/amaranth_ids.json`

### Generated data files

- `data/vtes.json` — all card data with rulings, translations, set info, image URLs
- `data/twda.json` — Tournament Winning Deck Archive in JSON
- `data/twd.htm` — normalized HTML TWDA
- `data/amaranth_ids.json` — Amaranth-to-KRCG card ID mapping

### Card images

~6,159 images in `static/card/`. Filenames are ASCII-only, lowercase, no spaces or punctuation (e.g., `powerbasezurich.jpg`). Crypt cards use symlinks (e.g., `theobellg2.jpg` → `theobell.jpg`), some vampires have multiple versions. The `CARD_RENAME` dict in `__init__.py` maps legacy filenames to canonical names.

## Testing

Tests live in `tests/test_static.py` with three test functions:
- `test_card()` — validates JSON output for specific cards (fields, disciplines, sets, rulings, i18n)
- `test_twda()` — validates JSON output for a specific TWDA deck
- `test_images()` — checks every card in VTES has a corresponding file in `static/card/` and no unexpected extras exist

`tests/conftest.py` loads VTES data from VEKN and TWDA from `tests/twda_test.html` (a 20-deck snapshot) at session start.

## Key Conventions

- Python 3.11+
- Formatter & Linter: `ruff` (default config)
- The `static/` directory including all card images and symlinks is committed to git
