.PHONY: quality test static update clean

export GITHUB_BRANCH = main
STATIC_SERVER ?= lpanhaleux@krcg.org:projects/static.krcg.org/dist

quality:
	black --check .
	flake8

test: quality
	pytest -vvs

static:
	krcg-static build
	rsync -rlptq --delete-after -e ssh build/ ${STATIC_SERVER}

minimal:
	krcg-static build --minimal
	rsync -rlptq --delete-after -e ssh build/ ${STATIC_SERVER}

update:
	pip install --upgrade --upgrade-strategy eager -e .[dev]

clean:
	rm -rf build
	rm -rf .pytest_cache
