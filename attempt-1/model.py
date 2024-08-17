# %% [markdown]
# ---
# title: "reprex for vetiver model load error"
# ---

# %%
import os
import vetiver
from vetiver import VetiverModel, vetiver_pin_write
from vetiver.data import mtcars
from sklearn.linear_model import LinearRegression
from sklearn.pipeline import Pipeline
from sklearn.base import BaseEstimator, TransformerMixin
from rsconnect.api import RSConnectServer
from dotenv import load_dotenv
from posit.connect import Client
from pins import board_rsconnect

load_dotenv()

with Client() as client:
    username = client.me.username


# %%
class MyTransformer(TransformerMixin, BaseEstimator):
    def fit(self, X, y=None):
        return self

    def transform(self, X):
        return X


model = Pipeline(
    steps=[("my_transformer", MyTransformer()), ("linear_model", LinearRegression())]
)
model.fit(mtcars.drop(columns="mpg"), mtcars["mpg"])
v = VetiverModel(
    model,
    model_name=f"{username}/cars_pipeline",
    prototype_data=mtcars.drop(columns="mpg"),
)
v.description


# %%
connect_server = RSConnectServer(
    url=os.environ["CONNECT_SERVER"],
    api_key=os.environ["CONNECT_API_KEY"],
)

board = board_rsconnect(allow_pickle_read=True)

vetiver_pin_write(board=board, model=v)

app_guid = os.getenv("APP_GUID")

vetiver.deploy_rsconnect(
    connect_server=connect_server,
    board=board,
    pin_name=f"{username}/cars_pipeline",
    extra_files=["requirements.txt"], 
    new=app_guid is None,
    app_id=app_guid,
)
