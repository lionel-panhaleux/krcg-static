.PHONY: quality test static update clean

export GITHUB_BRANCH = main
STATIC_SERVER ?= lpanhaleux@krcg.org:projects/static.krcg.org/dist

quality:
	black --check .
	ruff check

test: quality
	pytest -vv

static:
	krcg-static build
	rsync -rlptq --delete-after -e ssh build/ lpanhaleux@152.228.170.51:projects/static.krcg.org/dist
	rsync -rlptq --delete-after -e ssh build/ lpanhaleux@51.178.45.139:projects/static.krcg.org/dist

minimal:
	krcg-static build --minimal
	rsync -rlptq --delete-after -e ssh build/ ${STATIC_SERVER}

update:
	pip install --upgrade --upgrade-strategy eager -e .[dev,utils]

clean:
	rm -rf build
	rm -rf .pytest_cache
