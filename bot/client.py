import os
import requests
import time
import hmac
import hashlib
from urllib.parse import urlencode

from dotenv import load_dotenv
from bot.logging_config import setup_logger

load_dotenv()
logger = setup_logger()

class BinanceClient:
    """Handles auth, requests, error parsing"""

    def __init__(self):
        self.api_key = os.getenv("BINANCE_API_KEY")
        self.api_secret = os.getenv("BINANCE_API_SECRET")