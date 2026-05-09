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
        self.base_url = os.getenv("BINANCE_BASE_URL", "https://testnet.binancefuture.com")

        if not self.api_key or not self.api_secret:
            raise EnvironmentError(
                "Missing BINANCE_API_KEY or BINANCE_API_SECRET in .env file."
            )
        
        self.session = requests.Session()
        self.session.headers.update({
            "X-MBX-APIKEY":self.api_key,
            "Content-Type": "application/x-www-form-urlencoded"
        })

        logger.info(f"BinanceClient initialized. Base URL: {self.base_url}")

    def _generate_signature(self, params: dict) -> str:
        """
        Generates HMAC-SHA256 signature required by Binance for
        authenticated (SIGNED) endpoints.
        """
        query_string = urlencode(params)
        signature = hmac.new(
            self.api_secret.encode("utf-8"),
            query_string.encode("utf-8"),
            hashlib.sha256
        ).hexdigest()
        return signature

    def _get_timestamp(self) -> int:
        """Returns current UTC time in  milliseconds"""
        return int(time.time() * 1000)

    def send_signed_request(self, method: str, endpoint: str, params: dict = None) -> dict:
        if params is None:
            params = {}

        params["timestamp"] = self._get_timestamp()

        params["signature"] = self._generate_signature(params)

        url = f"{self.base_url}{endpoint}"

        logger.debug(f"REQUEST -> {method} {url}")
        logger.debug(f"PARAMS -> {self._safe_params(params)}")
        
        try:
            if method.upper() == "POST":
                response = self.session.post(url, data=params, timeout=10)
            elif method.upper() == "GET":
                response = self.session.get(url, params=params, timeout=10)
            else:
                raise ValueError(f"Unsupported HTTP method: {method}")
            
            logger.debug(f"RESPONSE STATUS -> {response.status_code}")
            logger.debug(f"RESPONSE BODY -> {response.text}")

            response.raise_for_status()

            data = response.json()

            if isinstance(data, dict) and "code" in data and data["code"] < 0:
                error_msg = f"Binance API Error {data['code']} : {data.get('msg', 'Unknown error')}"
                logger.error(error_msg)
                raise ValueError(error_msg)
            
            return data
        except requests.exceptions.ConnectionError as e:
            logger.error(f"Network connection error: {e}")
            raise
        except requests.exceptions.Timeout as e:
            logger.error(f"Request timed out: {e}")
            raise
        except requests.exceptions.HTTPError as e:
            try:
                error_data = response.json()
                msg = f"HTTP {response.status_code} | Binance: {error_data.get('code')} - {error_data.get('msg')}"
            except Exception:
                msg = f"HTTP Error: {e}"
            logger.error(msg)
            raise ValueError(msg)
        
    def _safe_params(self, params: dict) -> dict:
        safe = params.copy()
        if "signature" in safe:
            safe["signature"] = "***hidden***"
        return safe
    
    def get_account_info(self) -> dict:
        """Fetches account balance/info"""
        return self.send_signed_request("GET", "/fapi/v2/account")
    
    def get_exchange_info(self) -> dict:
        """Fetches exchange trading rules"""
        url = f"{self.base_url}/fapi/v1/exchangeInfo"
        response = self.session.get(url, timeout=10)
        response.raise_for_status()
        return response.json()
    