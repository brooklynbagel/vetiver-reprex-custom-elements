from vetiver import VetiverModel
from dotenv import load_dotenv, find_dotenv
from sklearn.base import BaseEstimator, TransformerMixin

import sys
import vetiver
import pins

load_dotenv(find_dotenv())


class MyTransformer(TransformerMixin, BaseEstimator):
    def fit(self, X, y=None):
        return self

    def transform(self, X):
        return X


setattr(sys.modules["__main__"], "MyTransformer", MyTransformer)


b = pins.board_connect(server_url="https://connect.posit.it", allow_pickle_read=True)
v = VetiverModel.from_pin(b, "michael.beigelmacher/cars_pipeline", version="578595")

vetiver_api = vetiver.VetiverAPI(v)
api = vetiver_api.app
