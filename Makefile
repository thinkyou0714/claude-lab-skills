PYTHON ?= python3

.PHONY: help install validate lint fmt test check all

help:
	@echo "make install   - 開発ツール（pytest, ruff）を導入"
	@echo "make validate  - 整合性検証（--strict + 内部リンク検査）"
	@echo "make lint      - ruff lint"
	@echo "make fmt       - ruff format"
	@echo "make test      - pytest"
	@echo "make check     - validate + lint + test（CI と同等）"

install:
	$(PYTHON) -m pip install pytest ruff

validate:
	$(PYTHON) validate_plugins.py --strict

lint:
	ruff check .

fmt:
	ruff format .

test:
	$(PYTHON) -m pytest

check: validate lint test

all: check
