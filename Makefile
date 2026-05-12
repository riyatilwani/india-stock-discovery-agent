PYTHON := .venv/bin/python
PIP := .venv/bin/pip

.PHONY: setup install run

setup:
	python3 -m venv .venv
	$(PIP) install -r requirements.txt

install:
	$(PIP) install -r requirements.txt

run:
	$(PYTHON) xai_finance_agent.py
