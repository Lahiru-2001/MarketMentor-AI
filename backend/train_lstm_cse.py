import os
import numpy as np
import pandas as pd
import torch
import yfinance as yf
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from ml.lstm.model import LSTMPricePredictor

SEQ_LENGTH = 20
MODEL_SAVE_PATH = "predict_price.pth"
DATASET_PATH = r"D:\My Projects\Python\MarketMentor-AI\backend\dataset"

# CSV files to load
FILES = [
    "JKH.csv",
    "HNB.csv"
    "NSB.csv",
    "CARG.csv",
    "DFCC.csv",
    "COMM.csv",
    "LLUB.csv",
    "HHL.csv",
    "DIAL.csv",
    "SAMP.csv",
    
]

# Corresponding symbols for real-time fetching
SYMBOLS = ["JKH", "HNB"]

def load_csv_prices(file_name):
    file_path = os.path.join(DATASET_PATH, file_name)
    try:
        df = pd.read_csv(file_path)
        df.columns = df.columns.str.strip()
        df = df.replace(",", "", regex=True)
        df["Close"] = pd.to_numeric(df["Close"], errors="coerce")
        df = df.dropna()
        df["Date"] = pd.to_datetime(df["Date"], format="%d-%b-%y")
        df = df.sort_values("Date")
        prices = df["Close"].values.astype(float)
        print(f"Loaded {file_name} | Rows: {len(prices)}")
        return prices
    except Exception as e:
        print("Error loading", file_name, e)
        return None

def fetch_realtime_prices(symbol, start="2020-01-01"):
    ticker = f"{symbol}.CM"
    try:
        df = yf.download(ticker, start=start, progress=False)
        if df.empty:
            print(f"No data for {symbol}")
            return None
        return df["Close"].values.astype(float)
    except Exception as e:
        print(f"Yahoo error {symbol}: {e}")
        return None

def create_sequences(prices, seq_length=SEQ_LENGTH):
    scaler = MinMaxScaler()
    scaled = scaler.fit_transform(prices.reshape(-1, 1))
    X, y = [], []
    for i in range(len(scaled) - seq_length):
        X.append(scaled[i:i + seq_length])
        y.append(scaled[i + seq_length])
    return np.array(X), np.array(y)

def train_lstm_all_stocks():
    print("Training using CSV + real-time data")

    all_X = []
    all_y = []

    # Load CSV files
    for file in FILES:
        prices = load_csv_prices(file)
        if prices is None:
            continue
        X, y = create_sequences(prices)
        all_X.append(X)
        all_y.append(y)

    # Fetch real-time data
    for symbol in SYMBOLS:
        prices = fetch_realtime_prices(symbol)
        if prices is None:
            continue
        X, y = create_sequences(prices)
        all_X.append(X)
        all_y.append(y)

    if len(all_X) == 0:
        print("No stock data found")
        return

    X = np.vstack(all_X)
    y = np.vstack(all_y)

    split = int(len(X) * 0.8)
    X_train = torch.tensor(X[:split], dtype=torch.float32)
    y_train = torch.tensor(y[:split], dtype=torch.float32)
    X_test = torch.tensor(X[split:], dtype=torch.float32)
    y_test = torch.tensor(y[split:], dtype=torch.float32)

    model = LSTMPricePredictor(input_size=1, hidden_size=64, num_layers=2)
    criterion = torch.nn.MSELoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=0.001)
    epochs = 50

    for epoch in range(epochs):
        model.train()
        optimizer.zero_grad()
        output = model(X_train)
        loss = criterion(output, y_train)
        loss.backward()
        optimizer.step()
        if (epoch + 1) % 10 == 0:
            print(f"Epoch {epoch+1}/{epochs} Loss: {loss.item():.6f}")

    model.eval()
    with torch.no_grad():
        predictions = model(X_test).numpy()
    y_test = y_test.numpy()

    mae = mean_absolute_error(y_test, predictions)
    rmse = np.sqrt(mean_squared_error(y_test, predictions))
    r2 = r2_score(y_test, predictions)

    print("\nModel Evaluation")
    print("MAE:", mae)
    print("RMSE:", rmse)
    print("R2:", r2)

    torch.save(model.state_dict(), MODEL_SAVE_PATH)
    print("\nModel saved:", MODEL_SAVE_PATH)

if __name__ == "__main__":
    train_lstm_all_stocks()