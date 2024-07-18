import pendulum

from airflow.decorators import dag, task
from airflow.models import Variable
from posit import connect


CONNECT_SERVER = Variable.get("CONNECT_SERVER")
CONNECT_API_KEY = Variable.get("CONNECT_API_KEY")

@dag(
    dag_id="example",
    schedule_interval="0 * * * *",
    start_date=pendulum.datetime(2021, 1, 1, tz="UTC"),
    catchup=False
)
def example():

    @task
    def etl():
        pass

    @task
    def restart():
        client = connect.Client(CONNECT_SERVER, CONNECT_API_KEY)
        content = client.content.get("5b6f05d1-1fea-480b-b8fa-51aec687a0bd")
        task = content.restart()
        if task:
            task.wait_for()

    @task
    def notification():
        pass

    etl() >> restart() >> notification()
example()
