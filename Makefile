.PHONY: static

STATIC_SERVER ?= krcg.org:projects/static.krcg.org/dist

static:
	krcg-static build
	rsync -rptov --delete-after -e ssh build/ ${STATIC_SERVER}
