from flask import Flask, jsonify
import requests
import time
import json
from threading import Lock

app = Flask(__name__)
window_size = 10
number_window = []
lock = Lock()

# Replace secrets.json content with recent response from the Authorization request
with open("secrets.json", "r") as file:
    token_data = json.load(file)

token_type = token_data.get("token_type", "Bearer")
access_token = token_data.get("access_token")

headers = {
    "Authorization": f"{token_type} {access_token}"
}


api_urls = {
    'p': 'http://20.244.56.144/evaluation-service/primes',
    'f': 'http://20.244.56.144/evaluation-service/fibo',
    'e': 'http://20.244.56.144/evaluation-service/even',
    'r': 'http://20.244.56.144/evaluation-service/rand'
}

def fetch_numbers(numberid):
    if numberid not in api_urls:
        return []

    try:
        start_time = time.time()
        response = requests.get(api_urls[numberid], headers=headers, timeout=0.5)
        duration = (time.time() - start_time) * 1000 

        if response.status_code == 200 and duration <= 500:
            return response.json().get("numbers", [])
        else:
            return []
    except requests.RequestException:
        return []

@app.route('/numbers/<numberid>', methods=['GET'])
def get_numbers(numberid):
    global number_window
    with lock:
        prev_window = number_window.copy()
        new_numbers = fetch_numbers(numberid)

        # Remove duplicates and maintain order
        for num in new_numbers:
            if num not in number_window:
                number_window.append(num) 

        if len(number_window) > window_size:
            number_window = number_window[-window_size:] # Keep only the last 'window_size' numbers

        curr_window = number_window.copy()

        if len(number_window) >= window_size:
            avg = round(sum(number_window) / window_size, 2)
        else:
            avg = round(sum(number_window) / len(number_window), 2) if number_window else 0.0

        return jsonify({
            "windowPrevState": prev_window,
            "windowCurrState": curr_window,
            "numbers": new_numbers,
            "avg": avg
        })

if __name__ == '__main__':
    app.run(port=9876)
