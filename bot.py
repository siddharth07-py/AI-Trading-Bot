from alpaca.data.historical import StockHistoricalDataClient, CryptoHistoricalDataClient
from alpaca.data.requests import StockBarsRequest, CryptoBarsRequest
from alpaca.data.timeframe import TimeFrame
from alpaca.trading.client import TradingClient
from alpaca.trading.requests import MarketOrderRequest, TakeProfitRequest, StopLossRequest
from alpaca.trading.enums import OrderSide, TimeInForce
import pandas as pd
import time
import requests # The library for Telegram messages

  # --- CONFIGURATION ---
API_KEY = "YOUR_ALPACA_API_KEY"
SECRET_KEY = "YOUR_ALPACA_SECRET_KEY"


# Telegram Config
TELEGRAM_TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"
CHAT_ID = "YOUR_CHAT_ID"

  # Trading Config
SYMBOL = "BTC/USD"
ASSET_TYPE = "crypto"
QTY_PERCENT = 0.02
STOP_LOSS_PCT = 0.005
TAKE_PROFIT_PCT = 0.01
FAST_SMA = 5
SLOW_SMA = 15

  # Initialize Clients
trading_client = TradingClient(API_KEY, SECRET_KEY, paper=True)
stock_client = StockHistoricalDataClient(API_KEY, SECRET_KEY)
crypto_client = CryptoHistoricalDataClient(API_KEY, SECRET_KEY)

def send_telegram_msg(message):
      """Sends a notification to your phone via Telegram."""
      try:
          url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
          payload = {"chat_id": CHAT_ID, "text": message}
          requests.post(url, data=payload)
      except Exception as e:
          print(f"⚠️ Telegram failed: {e}")

def get_sma(symbol, window):
      """Universal data fetcher."""
      try:
          if ASSET_TYPE == "stock":
              request = StockBarsRequest(symbol_or_symbols=symbol, timeframe=TimeFrame.Minute, limit=window)
              bars = stock_client.get_stock_bars(request).df
          else:
              request = CryptoBarsRequest(symbol_or_symbols=symbol, timeframe=TimeFrame.Minute, limit=window)
              bars = crypto_client.get_crypto_bars(request).df

          if bars.empty: return None
          return bars['close'].mean()
      except Exception as e:
          print(f"⚠️ Data Error: {e}")
          return None

def trade_logic():
    print(f"--- Scalping {SYMBOL} at {time.ctime()} ---")

    try:
          fast_avg = get_sma(SYMBOL, FAST_SMA)
          slow_avg = get_sma(SYMBOL, SLOW_SMA)

          if fast_avg is None or slow_avg is None:
              print("💤 Waiting for data feed...")
              return

          if ASSET_TYPE == "stock":
              current_price = stock_client.get_stock_bars(StockBarsRequest(symbol_or_symbols=SYMBOL,
  timeframe=TimeFrame.Minute, limit=1)).df['close'].iloc[-1]
          else:
              current_price = crypto_client.get_crypto_bars(CryptoBarsRequest(symbol_or_symbols=SYMBOL,
  timeframe=TimeFrame.Minute, limit=1)).df['close'].iloc[-1]

          print(f"Price: ${current_price:.2f} | Fast: ${fast_avg:.2f} | Slow: ${slow_avg:.2f}")

          try:
              position = trading_client.get_position(SYMBOL)
              has_position = True
          except:
              has_position = False

          if not has_position and fast_avg > slow_avg:
              print("⚡ SCALP SIGNAL: Buying...")
              account = trading_client.get_account()
              amount_to_risk = float(account.cash) * QTY_PERCENT

              # --- FIX: MINIMUM ORDER CHECK ---
              if amount_to_risk < 10:
                  print(f"⚠️ Trade skipped: Order value ${amount_to_risk:.2f} is below Alpaca's $10 minimum.")
                  return
              # --------------------------------

              qty = amount_to_risk / current_price

              if qty > 0:
                  order_data = MarketOrderRequest(
                      symbol=SYMBOL,
                      qty=round(qty, 4),
                      side=OrderSide.BUY,
                      time_in_force=TimeInForce.GTC,
                      take_profit=TakeProfitRequest(limit_price=round(current_price * (1 + TAKE_PROFIT_PCT), 2)),
                      stop_loss=StopLossRequest(stop_price=round(current_price * (1 - STOP_LOSS_PCT), 2))
                  )
                  trading_client.submit_order(order_data)

                  msg = f"🚀 BOT BUY!\nAsset: {SYMBOL}\nPrice: ${current_price:.2f}\nQty: {round(qty, 4)}\nTP:{TAKE_PROFIT_PCT*100}% | SL: {STOP_LOSS_PCT*100}%"
                  send_telegram_msg(msg)
                  print("Notification sent!")

          elif has_position and fast_avg < slow_avg:
              print("📉 TREND FAILED: Selling...")
              trading_client.close_position(SYMBOL)

              msg = f"📉 BOT SELL!\nAsset: {SYMBOL}\nTrend reversed. Position closed."
              send_telegram_msg(msg)
              print("Notification sent!")
          else:
              print("💤 Market flat. Waiting...")

    except Exception as e:
          print(f"⚠️ Unexpected Error: {e}")

  # --- START THE BOT ---
start_msg = f"🤖 Trading Bot is now ONLINE!\nMonitoring: {SYMBOL}\nStrategy: High-Frequency Scalper"
send_telegram_msg(start_msg)
print(f"Universal Scalper Active. Monitoring {SYMBOL}...")

while True:
      trade_logic()
      time.sleep(10)