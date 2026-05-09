import os
import hmac
import hashlib
import time
import requests
from urllib.parse import urlencode
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("BINANCE_API_KEY")
API_SECRET = os.getenv("BINANCE_API_SECRET")
BASE_URL = "https://testnet.binancefuture.com"

print(f"API Key: {API_KEY}")
print(f"API Key Length: {len(API_KEY) if API_KEY else 0}")
print(f"Secret Length: {len(API_SECRET) if API_SECRET else 0}")

# Test signed request
params = {"timestamp": int(time.time() * 1000)}
query_string = urlencode(params)
signature = hmac.new(
    API_SECRET.encode("utf-8"),
    query_string.encode("utf-8"),
    hashlib.sha256
).hexdigest()
params["signature"] = signature

headers = {"X-MBX-APIKEY": API_KEY}
response = requests.get(
    f"{BASE_URL}/fapi/v2/account",
    params=params,
    headers=headers
)

print(f"Status: {response.status_code}")
print(f"Response: {response.json()}")