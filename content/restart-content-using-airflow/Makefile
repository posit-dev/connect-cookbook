.DEFAULT_GOAL := all

.PHONY: \
	all\
	dev\
	down\
	init\
	up

AIRFLOW_UID := $(shell id -u)
DOCKER_COMPOSE ?= docker compose
PIP ?= pip

all: init dev up

clean:
	-$(DOCKER_COMPOSE) down --volumes --rmi all
	-rm -r ./logs .env airflow docker-compose.yaml
	-find . -name "*.egg-info" -exec rm -rf {} +
	-find . -name "*.pyc" -exec rm -f {} +
	-find . -name "__pycache__" -exec rm -rf {} +

dev:
	$(PIP) install -r requirements.txt

down:
	$(DOCKER_COMPOSE) down

init:
	curl -LfO 'https://airflow.apache.org/docs/apache-airflow/2.9.2/docker-compose.yaml'
	mkdir -p ./dags ./logs ./plugins ./config
	echo "AIRFLOW_UID=$(AIRFLOW_UID)" > .env
	curl -LfO 'https://airflow.apache.org/docs/apache-airflow/2.9.2/airflow.sh'
	chmod +x airflow.sh
	mv airflow.sh airflow

up:
	AIRFLOW_PROJ_DIR=. $(DOCKER_COMPOSE) up
