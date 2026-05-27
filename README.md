# 📈 AI Trading Bot

  An autonomous, high-frequency scalping bot designed for the Alpaca Markets API. This bot combines technical trend analysis
   with strict risk management to capture short-term price movements in the stock and crypto markets.

  ## 🚀 Features
  - **High-Frequency Scalping:** Operates on 1-minute timeframes to capture rapid price fluctuations.
  - **Trend-Following Logic:** Utilizes a Dual-SMA (Simple Moving Average) Crossover strategy (Fast 5m / Slow 15m).
  - **Professional Risk Management:**
    - **Bracket Orders:** Automatically sets Take-Profit and Stop-Loss targets at the moment of entry.
    - **Position Sizing:** Risks a fixed percentage of account equity per trade to prevent catastrophic loss.
    - **Trade Cooldown:** Implements a mandatory waiting period between trades to avoid "whipsawing" in choppy markets.
  - **Real-time Notifications:** Fully integrated with Telegram to send trade alerts directly to your phone.
  - **Cloud-Ready:** Optimized for 24/7 deployment on PythonAnywhere.

  ## 🛠️ Technical Stack
  - **Language:** Python 3.10+
  - **Broker API:** `alpaca-py` (Official SDK)
  - **Data Analysis:** `pandas`
  - **Networking:** `requests` (for Telegram API)

  ## 📦 Installation & Setup

  ### Prerequisites
  - An [Alpaca Markets](https://alpaca.markets/) account (Paper Trading enabled).
  - A Telegram Bot Token and Chat ID (via @BotFather and @userinfobot).
  - Python 3.10+ installed.

  ### Setup
  1. **Clone the repository:**
     ```bash
     git clone https://github.com/YOUR_USERNAME/imperium-capital-bot.git
     cd imperium-capital-bot

  2. Install dependencies:
  pip install alpaca-py pandas requests
  3. Configure your keys:
  Open bot.py and replace the placeholders with your actual credentials:
    - API_KEY
    - SECRET_KEY
    - TELEGRAM_TOKEN
    - CHAT_ID
  *Tip* - Try running handshake.py to authenticate the connection between Python and Alpaca API
  5. Run the bot:
  python bot.py

  ⚙️ Strategy Parameters

  You can tune the bot's behavior in the CONFIGURATION section of bot.py:
  - SYMBOL: The asset to trade (e.g., "AAPL" or "BTC/USD").
  - QTY_PERCENT: Percentage of cash to risk per trade (e.g., 0.02 for 2%).
  - STOP_LOSS_PCT: The "Emergency Brake" (e.g., 0.01 for 1%).
  - TAKE_PROFIT_PCT: The target gain (e.g., 0.01 for 1%).

  NOTE: If you want to make it fully automated, its suggested to run it on home server or cloud service providers through VPS
  
  ⚠️ Disclaimer

  This software is for educational and paper-trading purposes only. Trading involves significant risk of loss. The author is
   not responsible for any financial losses incurred while using this bot. Always test strategies in a paper environment
  before using real capital.

  ---Developed using Claude(free subscription)
