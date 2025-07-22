# lstm_predict.py
import sqlite3
import pandas as pd
import numpy as np
import time
from sklearn.preprocessing import MinMaxScaler
from keras.models import Sequential
from keras.layers import LSTM, Dense

def load_data():
    conn = sqlite3.connect('iot_data.db')
    query = "SELECT timestamp, temperature FROM tempData ORDER BY timestamp ASC" 
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

def preprocess_data(df):
    scaler = MinMaxScaler(feature_range=(0, 1)) 
    scaled_data = scaler.fit_transform(df[['temperature']])
    
    X, y = [], []
    seq_length = 5 
    for i in range(len(scaled_data) - seq_length):
        X.append(scaled_data[i:i+seq_length])
        y.append(scaled_data[i+seq_length])
        
    return np.array(X), np.array(y), scaler

def build_lstm_model(input_shape):
    model = Sequential([
        LSTM(50, return_sequences=True, input_shape=input_shape),
        LSTM(50),
        Dense(1) 
    ])
    model.compile(optimizer='adam', loss='mse') 
    return model

def get_latest_actual_value():
    conn = sqlite3.connect('iot_data.db')
    query = "SELECT timestamp, temperature FROM tempData ORDER BY timestamp DESC LIMIT 1" 
    df = pd.read_sql_query(query, conn)
    conn.close()
    if not df.empty:
        return df.iloc[0]['temperature'], df.iloc[0]['timestamp'] 
    return None, None


while True:
    print("\nTraining LSTM model...")
    df = load_data()
    
    if len(df) < 10:
        print("Not enough data to train. Need at least 10 entries.") 
    else:
        X, y, scaler = preprocess_data(df)
        model = build_lstm_model((X.shape[1], 1))
        model.fit(X, y, epochs=10, batch_size=16, verbose=0) 
        

        last_sequence = X[-1:]
        next_prediction = model.predict(last_sequence)
        predicted_temp = scaler.inverse_transform(next_prediction)[0][0] 
        

        actual_temp, actual_time = get_latest_actual_value() 
        
        print(f"Predicted next temperature: {predicted_temp:.2f}°C") 
        if actual_temp is not None:
            error = abs(predicted_temp - actual_temp)
            print(f"Latest actual temperature ({actual_time}): {actual_temp:.2f}°C") 
            print(f"Deviation: {error:.2f}°C") 
            
    time.sleep(10) 