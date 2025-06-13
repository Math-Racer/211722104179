from flask import Flask, request, jsonify
import requests
from headers import headers
from datetime import datetime, timedelta

app = Flask(__name__)

BASE_URL = "http://20.244.56.144/evaluation-service/stocks"

@app.route("/stocks/<ticker>")
def get_stock_price_history(ticker):
    try:
        minutes = int(request.args.get("minutes", 60))
        since_time = datetime.utcnow() - timedelta(minutes=minutes)

        
        response = requests.get(f"{BASE_URL}/{ticker}", headers=headers)
        if response.status_code != 200:
            return jsonify({"error": "Failed to fetch stock data"}), response.status_code

        all_prices = response.json()  
        filtered_prices = []

        for entry in all_prices:
            updated_time = datetime.fromisoformat(entry["lastUpdatedAt"].replace("Z", "+00:00"))
            if updated_time >= since_time:
                filtered_prices.append(entry)

        return jsonify({
            "ticker": ticker,
            "priceHistory": filtered_prices
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500



@app.route("/stocks/<ticker>/aggregation")
def incomplete_average_api(ticker):
    return "Not implemented yet", 501 # TODO: will implement after get_stock_price_history is working


if __name__ == "__main__":
    app.run(debug=True, port=9876)
