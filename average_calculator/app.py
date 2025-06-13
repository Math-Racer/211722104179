from flask import Flask, jsonify
import requests
import time
import json

app = Flask(__name__)

# Replace the secrets.json file content with new response you get from the authorization token
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
        duration = (time.time() - start_time) * 1000  # in ms

        if response.status_code == 200 and duration <= 500:
            return response.json().get("numbers", [])
        else:
            return []
    except requests.RequestException:
        return []

# Just fetch the numbers from the API and return them
@app.route('/numbers/<numberid>', methods=['GET'])
def get_numbers(numberid):
    numbers = fetch_numbers(numberid)
    return jsonify({
        "numbers": numbers
    })

if __name__ == '__main__':
    app.run(port=9876)
