import time
import requests
import yfinance as yf

# REPLACE THIS WITH YOUR UNIQUE NTFY TOPIC FROM STEP 1
NTFY_TOPIC = "alert-me-gold-stayp"
ALERT_DIRECTION = "above"  # Change to "below" if you want a drop alert


def get_target_price():
  try:
    # Reads the target price live from your GitHub config file
    url = (
        "https://raw.githubusercontent.com/thegreenzonemindset/My-Gold-Alert-Bot/main/config.txt"
    )
    # Note: Replace YOUR_USERNAME with your actual GitHub username above
    response = requests.get(url, timeout=10)
    return float(response.text.strip())
  except Exception as e:
    print(f"Could not read config file, using default: {e}")
    return 3000.0  # Fallback target


def send_push_notification(message):
  url = f"https://ntfy.sh/{NTFY_TOPIC}"
  requests.post(
      url,
      data=message.encode("utf-8"),
      headers={"Title": "⚠️ XAU/USD Price Alert!"},
  )


print("Checking XAU/USD price...")
target_price = get_target_price()
print(f"Current Target Price Loaded: {target_price}")

# Fetch live XAU/USD price using Yahoo Finance proxy (GC=F)
gold = yf.Ticker("GC=F")
todays_data = gold.history(period="1d", interval="1m")
current_price = todays_data["Close"].iloc[-1]

print(f"Live Gold Price: {current_price}")

# Evaluation
if ALERT_DIRECTION == "above" and current_price >= target_price:
  send_push_notification(
      f"Gold has crossed above ${target_price}! Current price: ${current_price:.2f}"
  )
  print("Alert sent: Price is above target.")
elif ALERT_DIRECTION == "below" and current_price <= target_price:
  send_push_notification(
      f"Gold has crossed below ${target_price}! Current price: ${current_price:.2f}"
  )
  print("Alert sent: Price is below target.")
else:
  print("Target not reached yet. No alert sent.")
