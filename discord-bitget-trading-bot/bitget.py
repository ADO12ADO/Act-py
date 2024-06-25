import requests
import time
import hmac
import hashlib
import json
import os
from dotenv import load_dotenv

load_dotenv()

BASE_URL = 'https://api.bitget.com/api'

HEADERS = {
    'Content-Type': 'application/json',
    'ACCESS-KEY': os.getenv('BITGET_API_KEY'),
    'ACCESS-PASSPHRASE': os.getenv('BITGET_API_PASSPHRASE'),
}

def get_signature(secret, timestamp, method, request_path, body):
    message = str(timestamp) + method + request_path + (json.dumps(body) if body else "")
    mac = hmac.new(bytes(secret, encoding='utf8'), bytes(message, encoding='utf-8'), digestmod=hashlib.sha256)
    return mac.hexdigest()

def place_order(token, entry_price, invalidation_level, target_prices, balance):
    side = 'buy' if entry_price < target_prices[0] else 'sell'
    quantity = (balance * 0.03) / entry_price
    leverage = max(1, int(balance / (entry_price - invalidation_level)))

    order = {
        "symbol": f"{token}USDT",
        "side": side,
        "type": "limit",
        "quantity": round(quantity, 4),
        "price": entry_price,
        "stopLoss": invalidation_level,
        "takeProfit": target_prices[0],
        "leverage": leverage
    }

    timestamp = int(time.time() * 1000)
    request_path = '/spot/v1/trade/orders'
    signature = get_signature(os.getenv('BITGET_API_SECRET'), timestamp, 'POST', request_path, order)

    HEADERS.update({
        'ACCESS-SIGN': signature,
        'ACCESS-TIMESTAMP': str(timestamp),
    })

    response = requests.post(BASE_URL + request_path, headers=HEADERS, json=order)

    if response.status_code == 200:
        print('Order placed:', response.json())
    else:
        print('Error placing order:', response.status_code, response.json())

if __name__ == "__main__":
    # Example usage:
    place_order('BTC', 30000, 29000, [31000], 10000)
