from bot.logging_config import setup_logger

logger = setup_logger()

VALID_SYMBOLS = [
    "BTCUSDT", "ETHUSDT", "BNBUSDT", "XRPUSDT",
    "ADAUSDT", "DOGEUSDT", "SOLUSDT", "LTCUSDT"
]

VALID_SIDES = ["BUY", "SELL"]
VALID_ORDER_TYPES = ["MARKET", "LIMIT", "STOP_MARKET"]

def validate_symbol(symbol: str) -> str:
    """
    Validates and normalizes the trading symbol
    """
    symbol = symbol.upper().strip()
    if symbol not in VALID_SYMBOLS:
        raise ValueError(
            f"Invalid symbol '{symbol}'."
            f"Valid options: {', '.join(VALID_SYMBOLS)}"
        )
    logger.debug(f"Symbol validated : {symbol}")
    return symbol

def validate_side(side: str) -> str:
    """Validates order side (BUY or SELL)."""
    side = side.upper().strip()
    if side not in VALID_SIDES:
        raise ValueError(
            f"Invalid side '{side}'. Must be one of: {', '.join(VALID_SIDES)}"
        )
    logger.debug(f"Side validated: {side}")
    return side

def validate_order_type(order_type: str) -> str:
    """Validates order type (MARKET, LIMIT, STOP_MARKET)."""
    order_type = order_type.upper().strip()
    if order_type not in VALID_ORDER_TYPES:
        raise ValueError(
            f"Invalid order type '{order_type}'. "
            f"Must be one of: {', '.join(VALID_ORDER_TYPES)}"
        )
    logger.debug(f"Order type validated: {order_type}")
    return order_type

def validate_quantity(quantity: str) -> float:
    """Validates quantity is a positive number"""
    try: 
        qty = float(quantity)
    except(ValueError, TypeError):
        raise ValueError(f"Quantity must be a number, got: '{quantity}'")
    
    if qty <= 0:
        raise ValueError(f"Quantitu must be greater than 0, got: {qty}")
    
    logger.debug(f"Quantity validated: {qty}")
    return qty

def validate_price(price: str) -> float:
    """Validates price is a positive number (for LIMIT orders)."""
    try:
        p = float(price)
    except (ValueError, TypeError):
        raise ValueError(f"Price must be a number, got: '{price}'")

    if p <= 0:
        raise ValueError(f"Price must be greater than 0, got: {p}")

    logger.debug(f"Price validated: {p}")
    return p

def validate_stop_price(stop_price: str) -> float:
    """Validates stop price for STOP_MARKET orders."""
    try:
        sp = float(stop_price)
    except (ValueError, TypeError):
        raise ValueError(f"Stop price must be a number, got: '{stop_price}'")

    if sp <= 0:
        raise ValueError(f"Stop price must be greater than 0, got: {sp}")

    logger.debug(f"Stop price validated: {sp}")
    return sp

def validate_all_inputs(symbol, side, order_ty, quantity, price=None, stop_price=None):
    """Master validation function"""
    validated = {}
    validated["symbol"] = validate_symbol(symbol)
    validated["side"] = validate_side(side)
    validated["order_type"] = validate_order_type(order_ty)
    validated["quantity"] = validate_quantity(quantity)

    if validated["order_type"] == "LIMIT":
        if price is None:
            raise ValueError("Price is required for LIMIT orders.")
        validated["price"] = validate_price(price)

    if validated["order_type"] == "STOP_MARKET":
        if stop_price is None:
            raise ValueError("Stop price is required for STOP_MARKET orders. Use --stop-price.")
        validated["stop_price"] = validate_stop_price(stop_price)

    logger.info(f"All inputs validated successfully: {validated}")
    return validated