export LOCAL_CARDS := "1"
static_server := env_var_or_default("STATIC_SERVER", "lpanhaleux@krcg.org:projects/static.krcg.org/dist")

quality:
    uv run ruff format --check .
    uv run ruff check

test: quality
    uv run pytest -vv

static:
    uv run krcg-static build
    rsync -rlptq --delete-after -e ssh build/ {{static_server}}

minimal:
    uv run krcg-static build --minimal
    rsync -rlptq --delete-after -e ssh build/ {{static_server}}

update:
    uv sync --extra dev

clean:
    rm -rf build
    rm -rf .pytest_cache
