from backend.ml.lstm.train import train_model
from sklearn.metrics import mean_squared_error
import numpy as np


def test_lstm_accuracy():

    model, scaler, X_test, y_test = train_model()

    predictions = model.predict(X_test)

    mse = mean_squared_error(y_test, predictions)

    rmse = np.sqrt(mse)

    print("LSTM RMSE:", rmse)

    assert rmse < 0.1