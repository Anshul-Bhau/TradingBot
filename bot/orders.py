from bot.client import BinanceClient
from bot.logging_config import setup_logger

logger = setup_logger()

class OrderManager:
    "Business logic, uses Binance client for API calls"

    def __init__(self, client: BinanceClient):
        self.client = client

    def place_market_order(self, symbol:str, side:str, quantity:float) -> dict:
        params = {
            "symbol" : symbol,
            "side" : side,
            "type" : "MARKET",
            "quantity" : quantity
        }
        
        logger.info(f"Placing MARKET order: {side} {quantity} {symbol}")
        response = self.client.send_signed_request("POST", "/fapi/v1/order", params)
        logger.info(f"MARKET order placed successfully. Order ID: {response.get('orderId')}")
        return response
    
    def place_limit_order(self, symbol:str, side:str, quantity:float, price:float) -> dict:
        params = {
            "symbol": symbol,
            "side": side,
            "type": "LIMIT",
            "quantity": quantity,
            "price": price,
            "timeInForce": "GTC",  # Good Till Cancelled 
        }

        logger.info(f"Placing LIMIT order: {side} {quantity} {symbol} @ {price}")
        response = self.client.send_signed_request("POST", "/fapi/v1/order", params)
        logger.info(f"LIMIT order placed successfully. Order ID: {response.get('orderId')}")
        return response

    def place_stop_market_order(self, symbol: str, side: str, quantity: float, stop_price: float) -> dict:
        params = {
            "symbol": symbol,
            "side": side,
            "type": "STOP_MARKET",
            "quantity": quantity,
            "stopPrice": stop_price,
        }

        logger.info(f"Placing STOP_MARKET order: {side} {quantity} {symbol} @ {stop_price}")
        response = self.client.send_signed_request("POST", "/fapi/v1/order", params)
        logger.info(f"STOP_MARKET order placed successfully. Order ID: {response.get('orderId')}")
        return response
    
    def place_order(self, validated_inputs: dict) -> dict:
        """Called by CLI with validated inputs"""

        order_type = validated_inputs["order_type"]
        symbol = validated_inputs["symbol"]
        side = validated_inputs["side"]
        quantity = validated_inputs["quantity"]

        if order_type == "MARKET":
            return self.place_market_order(symbol, side, quantity)
        
        if order_type == "MARKET":
            return self.place_market_order(symbol, side, quantity)

        elif order_type == "LIMIT":
            price = validated_inputs["price"]
            return self.place_limit_order(symbol, side, quantity, price)

        elif order_type == "STOP_MARKET":
            stop_price = validated_inputs["stop_price"]
            return self.place_stop_market_order(symbol, side, quantity, stop_price)

        else:
            raise ValueError(f"Unhandled order type: {order_type}")