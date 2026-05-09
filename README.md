# Binance Futures Testnet Trading Bot

A Python CLI application to place orders on Binance Futures Testnet (USDT-M).

## Setup

### 1. Clone and install
```bash
git clone https://github.com/yourusername/trading_bot.git
cd trading_bot
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Configure API keys
```bash
cp .env.example .env
# Edit .env and add your Binance Testnet API key and secret
```

Get keys from: https://testnet.binancefuture.com → API Key section

## Usage

### Market Order (Buy)
```bash
python cli.py --symbol BTCUSDT --side BUY --type MARKET --quantity 0.001
```

### Limit Order (Sell)
```bash
python cli.py --symbol ETHUSDT --side SELL --type LIMIT --quantity 0.01 --price 3000
```

### Stop-Market Order (Bonus)
```bash
python cli.py --symbol BTCUSDT --side SELL --type STOP_MARKET --quantity 0.001 --stop-price 40000
```

### Dry Run (validate without placing)
```bash
python cli.py --symbol BTCUSDT --side BUY --type MARKET --quantity 0.001 --dry-run
```

## Assumptions
- Testnet only — never use on real Binance account
- Quantities follow Binance minimum notional rules
- LIMIT orders use GTC (Good Till Cancelled) time-in-force
- Log file is at logs/trading_bot.log
- STOP_MARKET order type is implemented in code but 
  Binance Testnet does not fully support it on standard 
  endpoints. MARKET and LIMIT orders work fully.
