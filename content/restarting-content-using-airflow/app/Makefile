.DEFAULT_GOAL := all

.PHONY: all deps run

PIP ?= pip
SHINY ?= shiny

all: deps

clean:
	-find . -name "*.egg-info" -exec rm -rf {} +
	-find . -name "*.pyc" -exec rm -f {} +
	-find . -name "__pycache__" -exec rm -rf {} +

deps:
	$(PIP) install -r requirements.txt

run:
	$(SHINY) run app.py
