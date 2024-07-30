import pendulum
from airflow.decorators import dag, task
from airflow.models import Variable
from posit import connect

CONTENT_GUID = "a35ae786-16da-43c6-93d8-0c709766dc46"


@dag(
    dag_id="example",
    schedule_interval="0 * * * *",
    start_date=pendulum.now(),
    catchup=False,
)
def example():
    @task
    def restart():
        client = connect.Client(
            Variable.get("CONNECT_SERVER"), Variable.get("CONNECT_API_KEY")
        )
        content = client.content.get(CONTENT_GUID)
        content.restart()

    restart()


example()
