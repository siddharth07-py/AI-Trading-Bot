import alpaca_trade_api as tradeapi

  # --- YOUR KEYS GO HERE ---
API_KEY = "YOUR_ALPACA_API_KEY"
SECRET_KEY = "YOUR_ALPACA_SECRET_KEY"
BASE_URL = "https://paper-api.alpaca.markets" # This ensures we stay in Paper Trading (Fake Money)

try:
      # This is the 'Handshake' - it tries to log into your account
      api = tradeapi.REST(API_KEY, SECRET_KEY, BASE_URL, api_version='v2')

      # We ask the account for its balance to prove the connection is working
      account = api.get_account()

      print("✅ HANDSHAKE SUCCESSFUL!")
      print(f"Account Status: {account.status}")
      print(f"Current Buying Power: ${account.buying_power}")
      print(f"Cash Balance: ${account.cash}")
      print("\nYour bot can now see the markets. We are ready for the strategy!")

except Exception as e:
      print("❌ HANDSHAKE FAILED!")
      print(f"Error: {e}")
      print("\nDouble-check that your API keys are correct and that you are using the 'Paper Trading' keys, not the 'Live' keys.")
  