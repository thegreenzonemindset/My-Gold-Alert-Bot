import time
import requests
import yfinance as yf

# REPLACE THIS WITH YOUR UNIQUE NTFY TOPIC
NTFY_TOPIC = "alert-me-gold-stayp"
ALERT_DIRECTION = "above"  # Change to "below" if you want a drop alert


def get_target_price():
  try:
    url = "https://raw.githubusercontent.com/thegreenzonemindset/My-Gold-Alert-Bot/main/config.txt"
    response = requests.get(url, timeout=10)
    return float(response.text.strip())
  except Exception as e:
    print(f"Could not read config file, using default: {e}")
    return 3000.0


def send_push_notification(message):
  url = f"https://ntfy.sh/{NTFY_TOPIC}"
  requests.post(
      url,
      data=message.encode("utf-8"),
      headers={
          "Title": "⚠️ XAU/USD Price Alert!".encode("utf-8").decode(
              "latin-1"
          ),
          "Content-Type": "text/plain; charset=utf-8",
      },
  )


print("Checking XAU/USD price...")
target_price = get_target_price()
print(f"Current Target Price Loaded: {target_price}")

# Using a reliable spot/alternative gold data feed
try:
  # Gold spot tracker proxy or standard GLD proxy if GC=F fluctuates differently
  gold = yf.Ticker("GC=F")
  # Fetching daily data with a 5m interval for better accuracy
  todays_data = gold.history(period="2d", interval="5m")
  current_price = todays_data["Close"].iloc[-1]
except Exception as e:
  print(f"Error fetching from yfinance: {e}")
  current_price = 0.0

print(f"Live Gold Price: {current_price}")

# Evaluation
if current_price > 0:
  if ALERT_DIRECTION == "above" and current_price >= target_price:
    send_push_notification(
        f"Gold has crossed above ${target_price}! Current price:"
        f" ${current_price:.2f}"
    )
    print("Alert sent: Price is above target.")
  elif ALERT_DIRECTION == "below" and current_price <= target_price:
    send_push_notification(
        f"Gold has crossed below ${target_price}! Current price:"
        f" ${current_price:.2f}"
    )
    print("Alert sent: Price is below target.")
  else:
    print("Target not reached yet. No alert sent.")
