import pandas as pd
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
    def extract():
        iris = sns.load_dataset("iris", cache=False)
        iris.to_csv('/tmp/iris.csv', index=False)

    @task
    def transform():
        iris = pd.read_csv('/tmp/iris.csv')
        iris['petal_area'] = iris['petal_length'] * iris['petal_width']
        iris['sepal_area'] = iris['sepal_length'] * iris['sepal_width']
        iris.to_csv('/tmp/iris_transformed.csv', index=False)

    @task
    def load():
        iris_transformed = pd.read_csv('/tmp/iris_transformed.csv')
        client = connect.Client(CONNECT_SERVER, CONNECT_API_KEY)
        board = pins.board_connect(CONNECT_SERVER, api_key=CONNECT_API_KEY, cache=None)
        board.pin_write(
            iris_transformed,
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

    extract() >> transform() >> load() >> restart()
example()
