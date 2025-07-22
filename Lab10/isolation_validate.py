# isolation_validate.py
import sqlite3
import pandas as pd
import numpy as np
import time
from sklearn.ensemble import IsolationForest


def load_data():
    conn = sqlite3.connect('iot_data.db')
    query = "SELECT timestamp, temperature FROM tempData ORDER BY timestamp ASC"
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df


def train_anomaly_detector(df):
    model = IsolationForest(n_estimators=100, contamination=0.1, random_state=42) 
    model.fit(df[['temperature']]) 
    return model


def get_latest_entry():
    conn = sqlite3.connect('iot_data.db')
    query = "SELECT timestamp, temperature FROM tempData ORDER BY timestamp DESC LIMIT 1" 
    df = pd.read_sql_query(query, conn)
    conn.close()
    if not df.empty:
        return df.iloc[0] 
    return None


while True:
    print("\nChecking for anomalies in IoT data...")
    df = load_data()
    
    if len(df) < 10:
        print("Not enough data to check for anomalies.") 
    else:
        model = train_anomaly_detector(df)
        latest_entry = get_latest_entry() 
        
        if latest_entry is not None:

            latest_data = np.array([[latest_entry['temperature']]])
            prediction = model.predict(latest_data)[0]
            
            print(f"Latest data ({latest_entry['timestamp']}):") 
            print(f"  Temperature: {latest_entry['temperature']:.2f}°C") 
            

            if prediction == -1:
                print("  Status: WARNING: ANOMALY DETECTED!") 
            else:
                print("  Status: Valid data.") 
                
    time.sleep(10) 