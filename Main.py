import requests
import schedule
import time

# Bot setup
BOT_TOKEN = '7614359150:YOUR_FULL_BOT_TOKEN'
CHAT_ID = '897667750'

# SOXX monitoring function
def check_soxx():
    url = "https://query1.finance.yahoo.com/v8/finance/chart/SOXX"
    params = {
        "interval": "5m",
        "range": "1d"
    }
    response = requests.get(url, params=params)
    data = response.json()

    try:
        price = data['chart']['result'][0]['meta']['regularMarketPrice']
        message = f"**SOXX Update**\nCurrent Price: ${price:.2f}\n"

        if 170 <= price <= 174:
            message += "Entered resistance zone ($170–174). Watch for bearish signals to short."
        elif price < 170:
            message += "Below resistance zone. Monitoring for potential rebound."
        else:
            message += "Above resistance zone. Wait for setup."

        send_telegram_message(message)
    except Exception as e:
        send_telegram_message(f"SOXX bot error: {e}")

def send_telegram_message(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": text,
        "parse_mode": "Markdown"
    }
    requests.post(url, data=payload)

schedule.every(4).hours.do(check_soxx)
send_telegram_message("SOXX Bot started. Monitoring every 4 hours.")

while True:
    schedule.run_pending()
    time.sleep(10)
