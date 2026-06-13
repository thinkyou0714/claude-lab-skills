PYTHON ?= python3

.PHONY: help install validate lint fmt test typecheck lint-md fmt-md spell check check-docs all

help:
	@echo "make install   - 開発ツール（pytest, ruff, mypy, codespell）を導入"
	@echo "make validate  - 整合性検証（--strict + 内部リンク検査）"
	@echo "make lint      - ruff lint"
	@echo "make fmt       - ruff format"
	@echo "make typecheck - mypy 型チェック"
	@echo "make test      - pytest"
	@echo "make lint-md   - markdownlint（要 Node/npx）"
	@echo "make fmt-md    - markdownlint --fix"
	@echo "make spell     - codespell"
	@echo "make check     - validate + lint + typecheck + test（CI と同等）"
	@echo "make check-docs - lint-md + spell"

install:
	$(PYTHON) -m pip install pytest ruff mypy codespell

validate:
	$(PYTHON) validate_plugins.py --strict

lint:
	ruff check .

fmt:
	ruff format .

test:
	$(PYTHON) -m pytest

lint-md:
	npx --yes markdownlint-cli2@0.14.0 "**/*.md" "#node_modules"

fmt-md:
	npx --yes markdownlint-cli2@0.14.0 --fix "**/*.md" "#node_modules"

spell:
	codespell

typecheck:
	mypy

check: validate lint typecheck test

check-docs: lint-md spell

all: check check-docs
