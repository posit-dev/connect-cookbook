.DEFAULT_GOAL := all

.PHONY: all deps down init up

AIRFLOW_UID := $(shell id -u)
DOCKER_COMPOSE ?= docker compose
PIP ?= pip

all: init deps up

clean:
	-$(DOCKER_COMPOSE) down --volumes --rmi all
	-rm -r ./logs .env airflow docker-compose.yaml
	-find . -name "*.egg-info" -exec rm -rf {} +
	-find . -name "*.pyc" -exec rm -f {} +
	-find . -name "__pycache__" -exec rm -rf {} +

deps:
	$(PIP) install -r requirements.txt

down:
	$(DOCKER_COMPOSE) down

init:
	mkdir -p ./dags ./logs ./plugins ./config
	echo "AIRFLOW_UID=$(AIRFLOW_UID)" > .env

up:
	$(DOCKER_COMPOSE) up
