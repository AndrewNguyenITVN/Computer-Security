# iot_client.py
import requests
import random
import time
from datetime import datetime

server_url = "http://127.0.0.1:5000/upload" 

def generate_data():
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S") 
    temperature = round(random.uniform(15, 50), 2) 
    
    if temperature < 20:
        category = "Thấp" 
    elif temperature > 35:
        category = "Cao" 
    else:
        category = "Bình thường" 
        
    return {
        "timestamp": timestamp,
        "temperature": temperature,
        "category": category
    }


while True:
    data = generate_data()
    try:
        response = requests.post(server_url, json=data) 
        if response.status_code == 200:
            print(f"Sent: {data}") 
        else:
            print(f"Error: {response.status_code}")
    except requests.exceptions.ConnectionError as e:
        print(f"Error connecting to server: {e}")
        
    time.sleep(5) 