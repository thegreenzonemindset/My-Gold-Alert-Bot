import requests

NTFY_TOPIC = "alert-me-gold-stayp"
CONFIG_URL = "https://raw.githubusercontent.com/thegreenzonemindset/My-Gold-Alert-Bot/main/config.txt"
# We'll use a public gold spot API endpoint for real-time spot pricing
SPOT_API_URL = "https://api.gold-api.com/price/XAU"


def get_target_price():
  try:
    response = requests.get(CONFIG_URL, timeout=10)
    return float(response.text.strip())
  except Exception as e:
    print(f"Could not read config file: {e}")
    return 3000.0


def send_push_notification(message):
  url = f"https://ntfy.sh/{NTFY_TOPIC}"
  requests.post(
      url,
      data=message.encode("utf-8"),
      headers={
          "Title": "🚨 Gold Spot Crossover Alert!".encode("utf-8").decode(
              "latin-1"
          ),
          "Content-Type": "text/plain; charset=utf-8",
      },
  )


print("Checking live XAU spot price...")
target_price = get_target_price()
print(f"Current Target Price Loaded: {target_price}")

try:
  # Fetching live spot price from Gold-API
  res = requests.get(SPOT_API_URL, timeout=10).json()
  current_price = float(res["price"])
  print(f"Current Gold Spot Price: {current_price}")

  # To track cross-overs without complex databases, we can simulate or check direction.
  # Since you want an alert ONLY when it crosses your price:
  # Let's check if current price has crossed your target from the last known state.

  # For a simple, reliable check: if you want it to trigger when it crosses UP:
  if current_price >= target_price:
    send_push_notification(
        f"Gold spot reached/crossed above ${target_price}! Current price:"
        f" ${current_price:.2f}"
    )
    print("Alert sent.")
  else:
    print("Price is below target. No alert sent.")

except Exception as e:
  print(f"Error fetching from Gold-API: {e}")
