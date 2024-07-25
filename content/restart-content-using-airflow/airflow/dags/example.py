import pendulum
import pins
import seaborn as sns
from airflow.decorators import dag, task
from airflow.models import Variable
from posit import connect

CONNECT_SERVER = Variable.get("CONNECT_SERVER")
CONNECT_API_KEY = Variable.get("CONNECT_API_KEY")


@dag(
    dag_id="example",
    schedule_interval="0 * * * *",
    start_date=pendulum.datetime(2021, 1, 1, tz="UTC"),
    catchup=False,
)
def example():
    @task
    def load():
        client = connect.Client(CONNECT_SERVER, CONNECT_API_KEY)
        board = pins.board_connect(CONNECT_SERVER, api_key=CONNECT_API_KEY, cache=None)

        iris = sns.load_dataset("iris", cache=False)
        board.pin_write(
            iris,
            name=f"{client.me.username}/iris_dataset",
            type="csv",
            description="Iris dataset for demonstration purposes.",
        )

    @task
    def restart():
        client = connect.Client(CONNECT_SERVER, CONNECT_API_KEY)
        content = client.content.find()
        content = next(
            item
            for item in content
            if item.title == "Airflow Example - Shiny Application"
        )
        content.restart()

    @task
    def notification():
        pass

    load() >> restart() >> notification()
example()
