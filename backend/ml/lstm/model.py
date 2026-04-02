from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout, Input


# Function to build and return an LSTM model
def build_lstm_model(input_shape):

    # Create a Sequential neural network model
    model = Sequential()

    # Define input shape for the model
    model.add(Input(shape=input_shape))

    # First LSTM layer with 128 units
    model.add(LSTM(128, return_sequences=True))

    # Dropout layer to reduce overfitting by randomly disabling 30% neurons
    model.add(Dropout(0.3))

    # Second LSTM layer with 64 units
    # Still returns sequences because another LSTM layer follows
    model.add(LSTM(64, return_sequences=True))

    # Dropout again for regularization
    model.add(Dropout(0.3))

    # Third LSTM layer with 32 units
    # return_sequences=False by default because this is last LSTM layer
    model.add(LSTM(32))

    # Dropout layer after final LSTM layer
    model.add(Dropout(0.2))

    # Dense hidden layer with ReLU activation for feature learning
    model.add(Dense(16, activation="relu"))

    # Output layer with 1 neuron for prediction (regression output)
    model.add(Dense(1))

    # Compile model  
    model.compile(
        optimizer="adam",
        loss="mean_squared_error",
        metrics=["mae"]
    )

    # Return completed model
    return model