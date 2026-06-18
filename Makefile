PYTHON := .venv/bin/python
PIP := .venv/bin/pip
API := .venv/bin/uvicorn

.PHONY: setup install run api web

setup:
	python3 -m venv .venv
	$(PIP) install -r requirements.txt
	cd frontend && npm install

install:
	$(PIP) install -r requirements.txt
	cd frontend && npm install

run: api

api:
	$(API) backend.app.main:app --reload --host 0.0.0.0 --port 8000

web:
	cd frontend && npm run dev

legacy-agent:
	$(PYTHON) xai_finance_agent.py
