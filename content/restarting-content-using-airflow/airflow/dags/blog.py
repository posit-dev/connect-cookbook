import datetime

import pins
import seaborn as sns
from airflow.decorators import dag, task
from airflow.models import Variable
from posit import connect
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import LabelEncoder, StandardScaler

CONNECT_SERVER = Variable.get("CONNECT_SERVER")
CONNECT_API_KEY = Variable.get("CONNECT_API_KEY")
CONNECT_USER_NAME = "taylor_steinberg"
CONNECT_CONTENT_ID = "20b84ee4-f623-4a30-9a08-3c678aceb22f"


@task
def prepare_data():
    penguins = sns.load_dataset("penguins", cache=False)
    penguins = penguins.dropna()
    encoder = LabelEncoder()
    penguins["species"] = encoder.fit_transform(penguins["species"])
    return {"penguins": penguins, "encoder": encoder}


@task
def train_model(data):
    penguins = data["penguins"]
    encoder = data["encoder"]
    X = penguins[
        ["bill_length_mm", "bill_depth_mm", "flipper_length_mm", "body_mass_g"]
    ]
    y = penguins["species"]
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=0
    )
    pipeline = Pipeline([("scaler", StandardScaler()), ("model", LogisticRegression())])
    pipeline.fit(X_train, y_train)
    return {"pipeline": pipeline, "encoder": encoder, "X_test": X_test, "y_test": y_test}


@task
def evaluate_model(data):
    pipeline = data["pipeline"]
    X_test = data["X_test"]
    y_test = data["y_test"]
    score = pipeline.score(X_test, y_test)
    print(f"Model score: {score}")
    if score < 0.9:
        print("Model score does not meet 90% threshold")
        return False
    print("Model score meets 90% threshold")
    return True


@task
def deploy_model(data, is_valid):
    if not is_valid:
        print("Skipping deployment")
        return False
    print("Deploying model")
    encoder = data["encoder"]
    pipeline = data["pipeline"]
    board = pins.board_connect(CONNECT_SERVER, api_key=CONNECT_API_KEY, cache=None, allow_pickle_read=True)
    board.pin_write(encoder, name=f"{CONNECT_USER_NAME}/encoder", type="joblib")
    board.pin_write(pipeline, name=f"{CONNECT_USER_NAME}/pipeline", type="joblib")
    return True


@task
def restart_app(is_deployed):
    if not is_deployed:
        print("Skipping restart")
        return
    client = connect.Client(CONNECT_SERVER, CONNECT_API_KEY)
    content = client.content.get(CONNECT_CONTENT_ID)
    print(f"Restarting {content.dashboard_url}")
    content.restart()


@dag(catchup=False, start_date=datetime.datetime(2021, 1, 1), schedule="@daily")
def penguins_dag():
    data = prepare_data()
    model_data = train_model(data)
    is_valid = evaluate_model(model_data)
    is_deployed = deploy_model(model_data, is_valid)
    restart_app(is_deployed)


penguins_dag()
