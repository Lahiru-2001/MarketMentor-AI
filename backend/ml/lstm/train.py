import os
import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from tensorflow.keras.callbacks import EarlyStopping
from backend.ml.lstm.model import build_lstm_model
from backend.api_clients.twelve_data import get_time_series
from backend.api_clients.cse import get_cse_share_price

# PATHS FOR DATA AND MODEL
DATASET_PATH = "backend/ml/lstm/stock_dataset.csv" 
MODEL_PATH = "backend/ml/lstm/stock_lstm_model.keras"  

# Global stock symbols (major international stocks)
GLOBAL_SYMBOLS = [
    "AAPL","MSFT","GOOGL","AMZN","TSLA","META","NVDA",
    "NFLX","AMD","INTC","ORCL","IBM","BABA","UBER","SHOP"
]

# Colombo Stock Exchange symbols (Sri Lankan stocks)
CSE_SYMBOLS = [
    "JKH","LOLC","COMB","SAMP","HNB","DIAL","SLT","EXPO"
]

# FETCH GLOBAL DATA FUNCTION
def fetch_global_data(symbol):
    """
    Fetch historical time series data for a global stock symbol
    using the Twelve Data API client.
    Returns a pandas DataFrame with columns: open, high, low, close, volume
    """

    try:
        data = get_time_series(symbol) # fetch data from API client

        rows = []
        for row in data["values"]:
            rows.append({
                "open": float(row["open"]),
                "high": float(row["high"]),
                "low": float(row["low"]),
                "close": float(row["close"]),
                "volume": float(row.get("volume",0))  # some APIs may not return volume
            })

        return pd.DataFrame(rows) # convert list of dicts to DataFrame

    except Exception as e:
        print("Error fetching", symbol, e)
        return pd.DataFrame()  # return empty DataFrame if API call fails

# FETCH CSE DATA FUNCTION
def fetch_cse_data(symbol):
    """
    Fetch the latest share price for a CSE stock symbol
    using the CSE API client.
    Returns a pandas DataFrame with columns: open, high, low, close, volume
    """
    try:
        data = get_cse_share_price(symbol)

        return pd.DataFrame([{
            "open": data["last_trade_price"],
            "high": data["last_trade_price"],
            "low": data["last_trade_price"],
            "close": data["last_trade_price"],
            "volume": data["volume"]
        }])

    except:
        return pd.DataFrame()  # return empty DataFrame if API call fails

# BUILD DATASET FUNCTION
def build_dataset():
    """
    Fetch all global and CSE stock data and combine into a single DataFrame.
    Saves the dataset as a CSV file for caching.
    """

    all_frames = []

    print("Downloading global stocks...")
    for symbol in GLOBAL_SYMBOLS:
        df = fetch_global_data(symbol)
        if not df.empty:
            df["symbol"] = symbol  # add symbol column
            all_frames.append(df)

    print("Downloading CSE stocks...")
    for symbol in CSE_SYMBOLS:
        df = fetch_cse_data(symbol)
        if not df.empty:
            df["symbol"] = symbol
            all_frames.append(df) 

    dataset = pd.concat(all_frames)  # combine all data into one DataFrame
    dataset.to_csv(DATASET_PATH, index=False)  # save to CSV for reuse
    print("Dataset saved:", DATASET_PATH)

    return dataset



# LOAD DATASET FUNCTION
def load_dataset():
    """
    Load dataset from CSV if available.
    Otherwise, fetch new data and build dataset.
    """
    if os.path.exists(DATASET_PATH):
        print("Loading cached dataset...")
        return pd.read_csv(DATASET_PATH)

    return build_dataset()



# ADD TECHNICAL INDICATORS FUNCTION
def add_technical_indicators(df):
    """
    Add simple technical indicators for model input:
    - 10-day moving average (ma10)
    - 50-day moving average (ma50)
    - 10-day volatility (standard deviation)
    """
    df["ma10"] = df["close"].rolling(window=10).mean()
    df["ma50"] = df["close"].rolling(window=50).mean()
    df["volatility"] = df["close"].rolling(window=10).std() # Measures market instability.

    df = df.bfill()  # backfill missing values at the start

    return df



# CREATE SEQUENCES FUNCTION
def create_sequences(data, window=120):
    """
    Convert time series data into sequences suitable for LSTM:
    - X: sequence of 'window' timesteps
    - y: next closing price
    """
    X = [] 
    y = []

    for i in range(window, len(data)): 
        X.append(data[i-window:i]) 
        y.append(data[i,3])  # close price is the 4th column

    return np.array(X), np.array(y)


# TRAIN MODEL FUNCTION
def train_model():
    """
    Load data, preprocess, create sequences, train an LSTM model,
    and save the trained model.
    """

    df = load_dataset()
    df = add_technical_indicators(df)

    # Select features for model training
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

    scaler = MinMaxScaler()
    scaled_data = scaler.fit_transform(features)  # scale features to [0,1]

    # Create sequences for LSTM
    X, y = create_sequences(scaled_data)

    # Train/test split without shuffling to preserve time series order
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, shuffle=False # False is correct for time series.
    )

    # Build LSTM model (120, 8) input shape
    model = build_lstm_model((X_train.shape[1], X_train.shape[2]))

    # Early stopping to prevent overfitting
    early_stop = EarlyStopping(
        monitor="val_loss", # monitor validation loss to determine when to stop
        patience=5, # stop training if no improvement for 5 epochs
        restore_best_weights=True # restore the model weights from the epoch with the best validation loss
    ) 

    # Train the model
    model.fit(
        X_train,  
        y_train,
        validation_data=(X_test, y_test), 
        epochs=50, 
        batch_size=32, 
        callbacks=[early_stop]
    )

    # Evaluate model performance
    predictions = model.predict(X_test) # generate predictions on the test set
    rmse = np.sqrt(mean_squared_error(y_test, predictions))
    print("Model RMSE:", rmse)

    # Save the trained model
    model.save(MODEL_PATH)
    print("Model saved to:", MODEL_PATH)

    return model



# MAIN SCRIPT EXECUTION
if __name__ == "__main__":
    train_model()