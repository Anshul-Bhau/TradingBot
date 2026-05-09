"""
Trading Bot CLI — Entry Point

Usage examples:
    python cli.py --symbol BTCUSDT --side BUY --type MARKET --quantity 0.001
    python cli.py --symbol ETHUSDT --side SELL --type LIMIT --quantity 0.01 --price 3000
    python cli.py --symbol BTCUSDT --side SELL --type STOP_MARKET --quantity 0.001 --stop-price 40000
"""

import argparse
import json 
import sys

from bot.client import BinanceClient
from bot.logging_config import setup_logger
from bot.orders import OrderManager
from bot.validators import validate_all_inputs

logger = setup_logger()

def print_order_summary(validated: dict):
    print("\n" + "=" * 50)
    print("        ORDER SUMMARY (Before Submission)")
    print("=" * 50)
    print(f"  Symbol     : {validated['symbol']}")
    print(f"  Side       : {validated['side']}")
    print(f"  Order Type : {validated['order_type']}")
    print(f"  Quantity   : {validated['quantity']}")
    if "price" in validated:
        print(f"  Price      : {validated['price']}")
    if "stop_price" in validated:
        print(f"  Stop Price : {validated['stop_price']}")
    print("=" * 50)

def print_order_response(response: dict):
    """Prints key details from Binance's order response."""
    print("\n" + "=" * 50)
    print("        ORDER RESPONSE (From Binance)")
    print("=" * 50)
    print(f"  Order ID     : {response.get('orderId', 'N/A')}")
    print(f"  Symbol       : {response.get('symbol', 'N/A')}")
    print(f"  Status       : {response.get('status', 'N/A')}")
    print(f"  Side         : {response.get('side', 'N/A')}")
    print(f"  Type         : {response.get('type', 'N/A')}")
    print(f"  Quantity     : {response.get('origQty', 'N/A')}")
    print(f"  Executed Qty : {response.get('executedQty', 'N/A')}")
    print(f"  Avg Price    : {response.get('avgPrice', 'N/A')}")
    print(f"  Time in Force: {response.get('timeInForce', 'N/A')}")
    print("=" * 50)
    print(f"\n  Full response saved to log file: logs/trading_bot.log\n")

def build_parser() -> argparse.ArgumentParser:
    """Defines and returns the argument parser."""
    parser = argparse.ArgumentParser(
        prog="trading_bot",
        description="Binance Futures Testnet Trading Bot",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Market Buy
  python cli.py --symbol BTCUSDT --side BUY --type MARKET --quantity 0.001

  # Limit Sell
  python cli.py --symbol ETHUSDT --side SELL --type LIMIT --quantity 0.01 --price 3000

  # Stop-Market (Bonus order type)
  python cli.py --symbol BTCUSDT --side SELL --type STOP_MARKET --quantity 0.001 --stop-price 40000
        """
    )

    parser.add_argument(
        "--symbol", "-s",
        required=True,
        help="Trading pair symbol, e.g. BTCUSDT"
    )
    parser.add_argument(
        "--side",
        required=True,
        choices=["BUY", "SELL", "buy", "sell"],
        help="Order side: BUY or SELL"
    )
    parser.add_argument(
        "--type", "-t",
        dest="order_type",
        required=True,
        choices=["MARKET", "LIMIT", "STOP_MARKET", "market", "limit", "stop_market"],
        help="Order type: MARKET, LIMIT, or STOP_MARKET"
    )
    parser.add_argument(
        "--quantity", "-q",
        required=True,
        help="Quantity to trade (e.g. 0.001 for BTC)"
    )
    parser.add_argument(
        "--price", "-p",
        required=False,
        default=None,
        help="Limit price (required for LIMIT orders)"
    )
    parser.add_argument(
        "--stop-price",
        required=False,
        default=None,
        dest="stop_price",
        help="Stop trigger price (required for STOP_MARKET orders)"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Validate inputs and show summary without placing the order"
    )

    return parser

def main():
    parser = build_parser()
    args = parser.parse_args()

    logger.info("=" * 60)
    logger.info("Trading Bot started")
    logger.info(f"Raw args: symbol={args.symbol}, side={args.side}, "
                f"type={args.order_type}, qty={args.quantity}, "
                f"price={args.price}, stop_price={args.stop_price}")
    
    try:
        validated = validate_all_inputs(
            symbol=args.symbol,
            side=args.side,
            order_type=args.order_type,
            quantity=args.quantity,
            price=args.price,
            stop_price=args.stop_price,
        )
    except ValueError as e:
        logger.error(f"Input validation failed: {e}")
        print(f"\n Validation Error: {e}\n")
        sys.exit(1)

    print_order_summary(validated)

    if args.dry_run:
        print("\n DRY RUN mode - order NOT submitted. \n")
        logger.info("Dry run mode - existing without placing order.")
        sys.exit(0)

    try:
        client = BinanceClient()
        manager = OrderManager(client)
        response = manager.place_order(validated)

    except EnvironmentError as e:
        logger.error(f"Configuration error: {e}")
        print(f"\n Config Error: {e}\n")
        sys.exit(1)

    except ValueError as e:
        logger.error(f"Order placement failed (API error): {e}")
        print(f"\n API Error: {e}\n")
        sys.exit(1)

    except Exception as e:
        logger.error(f"Unexpected error: {e}", exc_info=True)
        print(f"\n Unexpected Error: {e}\n")
        sys.exit(1)

    logger.info(f"Order response: {json.dumps(response)}")
    print_order_response(response)
    print("Order placed successfully!\n")
    logger.info("Trading Bot session ended successfully.")

if __name__ == "__main__":
    main()