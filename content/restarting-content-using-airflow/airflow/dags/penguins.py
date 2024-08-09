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
    dag_id="penguins",
    schedule_interval="0 * * * *",
    start_date=pendulum.now(),
    catchup=False,
)
def penguins_dag():

    @task
    def extract():
        penguins = sns.load_dataset("penguins", cache=False)
        penguins.to_csv('/tmp/penguins.csv', index=False)

    @task
    def transform():
        penguins = pd.read_csv('/tmp/penguins.csv')
        penguins = penguins.sample(500, replace=True)
        penguins.to_csv('/tmp/penguins.csv', index=False)

    @task
    def load():
        penguins = pd.read_csv('/tmp/penguins.csv')
        client = connect.Client(CONNECT_SERVER, CONNECT_API_KEY)
        board = pins.board_connect(CONNECT_SERVER, api_key=CONNECT_API_KEY, cache=None)
        board.pin_write(
            penguins,
            name=f"{client.me.username}/penguins",
            type="csv",
            description="Penguins dataset for demonstration purposes.",
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
        print(content.dashboard_url)

    extract() >> transform() >> load() >> restart()
penguins_dag()
