import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import load_model
from backend.ml.lstm.train import add_technical_indicators


# Path to saved trained LSTM model
MODEL_PATH = "backend/ml/lstm/stock_lstm_model.keras"
# Number of previous time steps used for prediction
WINDOW = 120


def predict_price(prices: list) -> float:
    """
    Predict next stock price using trained LSTM model.

    Parameters:
        prices (list): Historical stock closing prices

    Returns:
        float: Predicted next stock price
    """

    # Load trained LSTM model
    model = load_model(MODEL_PATH)

    # If not enough data for prediction window,return latest available price
    if len(prices) < WINDOW:
        return prices[-1]

    # Create dataframe
    df = pd.DataFrame({
        "open": prices,
        "high": prices,
        "low": prices,
        "close": prices,
        "volume": [1000] * len(prices)
    })

    # Add technical indicators:
    df = add_technical_indicators(df)

    # Select features used during training
    features = df[
        [
            "open",
            "high",
            "low",
            "close",
            "volume",
            "ma10",
            "ma50",
            "volatility"
        ]
    ]

    # Normalize features to improve model performance
    scaler = MinMaxScaler()
    scaled = scaler.fit_transform(features)

    # Prepare last WINDOW rows as model input
    # Shape becomes (1, WINDOW, number_of_features)
    X = np.array([scaled[-WINDOW:]])

    # Predict normalized next closing price
    pred = model.predict(X, verbose=0)

    # Retrieve original close price min and max for inverse scaling of predicted value
    close_min = scaler.data_min_[3]
    close_max = scaler.data_max_[3]

    # Convert predicted normalized value back to original price scale
    predicted = pred[0][0] * (close_max - close_min) + close_min

    # Return rounded predicted price
    return round(float(predicted), 2)