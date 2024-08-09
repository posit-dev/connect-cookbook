FROM apache/airflow:2.9.2

USER root
RUN apt-get update && \
    apt-get install -y git && \
    apt-get clean

USER airflow
ADD requirements.txt .
RUN pip install apache-airflow==${AIRFLOW_VERSION} -r requirements.txt
