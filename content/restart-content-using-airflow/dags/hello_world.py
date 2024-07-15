from airflow import DAG
from airflow.decorators import task
from datetime import datetime, timedelta

# Define the default_args dictionary
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# Define the DAG
dag = DAG(
    'hello_world',
    default_args=default_args,
    description='A simple hello world DAG',
    schedule_interval=timedelta(days=1),
    start_date=datetime(2023, 7, 1),
    catchup=False,
)

# Define the Python function to be executed using the task decorator
@task(dag=dag)
def hello_world():
    print("Hello, World!")

# Define the task
hello_world_task = hello_world()

# Set task dependencies if necessary (not needed for a single task)
