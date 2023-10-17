default: help

.PHONY: help test run dev

help: # Show help for each of the Makefile recipes.
	@grep -E '^[a-zA-Z0-9 -]+:.*#'  Makefile | while read -r l; do printf "\033[1;32m$$(echo $$l | cut -f 1 -d':')\033[00m:$$(echo $$l | cut -f 2- -d'#')\n"; done

test: # run unit test for backend service
	python -m unittest

run: # run service without reload flag
	uvicorn main:app

dev: # run service with reload flag
	uvicorn main:app --reload

