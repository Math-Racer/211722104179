import requests
from flask import Flask, request, jsonify
import datetime
from headers import headers  

app = Flask(__name__)

API_URL = "http://20.244.56.144/evaluation-service/stocks/"

@app.route('/stocks/<ticker>', methods=['GET'])
def get_average_stock_price(ticker):
    minutes = int(request.args.get('minutes', 0))

    response = requests.get(f"{API_URL}{ticker}", headers=headers)
    data = response.json()

    prices = [p['price'] for p in data['priceHistory'] if within_last_m_minutes(p['lastUpdatedAt'], minutes)]
    
    avg_price = sum(prices) / len(prices) if prices else 0

    return jsonify({
        "averageStockPrice": avg_price,
        "priceHistory": prices
    })

def within_last_m_minutes(timestamp, m):
    dt = datetime.datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%S.%fZ")
    return (datetime.datetime.utcnow() - dt).seconds <= (m * 60)

if __name__ == '__main__':
    app.run(debug=True)