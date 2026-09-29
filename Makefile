.PHONY: help install asset-data asset test lint format serve clean

VENV   := .venv
PYTHON := python3.11
BIN    := $(VENV)/bin
PIP    := $(BIN)/pip
PY     := $(BIN)/python
LINTED := src/asset tests src/pipeline/export_asset.py src/pipeline/embed_asset.py src/pipeline/fetch_asset_data.py

help:
	@echo "swiss-governance-dashboard — common commands"
	@echo ""
	@echo "  make install     Create .venv (python3.11) and install the asset pipeline + dev tools"
	@echo "  make asset-data  Fetch/cache the City of Zurich open-data CSVs (data/raw/, idempotent)"
	@echo "  make asset       Export data/processed/asset_hagenholz.json and embed it in dashboard_real.html"
	@echo "  make test        Run pytest (data-contract tests skip if data is not cached)"
	@echo "  make lint        ruff check + format check on the asset code"
	@echo "  make format      Apply ruff format & autofixes"
	@echo "  make serve       Serve the cockpit on http://127.0.0.1:9000/dashboard_real.html"
	@echo "  make clean       Remove caches and the virtualenv"

$(BIN)/python:
	$(PYTHON) -m venv $(VENV)
	$(PIP) install --upgrade pip wheel

install: $(BIN)/python
	$(PIP) install -e ".[asset,dev]"

asset-data:
	$(PY) src/pipeline/fetch_asset_data.py

asset:
	$(PY) src/pipeline/export_asset.py
	$(PY) src/pipeline/embed_asset.py

test:
	$(BIN)/pytest -v

lint:
	$(BIN)/ruff check $(LINTED)
	$(BIN)/ruff format --check $(LINTED)

format:
	$(BIN)/ruff check --fix $(LINTED)
	$(BIN)/ruff format $(LINTED)

serve:
	python3 -m http.server 9000 --bind 127.0.0.1

clean:
	rm -rf $(VENV) build dist *.egg-info .pytest_cache .ruff_cache .coverage htmlcov
	find . -type d -name __pycache__ -exec rm -rf {} +
