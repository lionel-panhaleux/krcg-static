.PHONY: static

STATIC_SERVER ?= krcg.org:projects/static.krcg.org/dist

static:
	krcg-static build
	rsync -rptq --delete-after -e ssh build/ ${STATIC_SERVER}
