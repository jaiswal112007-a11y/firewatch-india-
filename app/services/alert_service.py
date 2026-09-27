import requests
import os
from dotenv import load_dotenv

env_path = os.path.join(os.path.dirname(__file__), '../../.env')
load_dotenv(dotenv_path=env_path)

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

def send_telegram_alert(fire_type, lat, lon, frp, confidence, date):
    """Send Telegram alert for high priority fires"""
    try:
        # Priority level
        if frp and frp > 100:
            priority = "🔴 CRITICAL"
        else:
            priority = "🟠 HIGH"

        # Fire emoji
        emoji = {
            'Industrial Fire': '🏭',
            'Gas Flare': '🔥',
            'Wildfire': '🌲',
            'Agricultural Burning': '🌾'
        }.get(fire_type, '🔥')

        message = f"""
🚨 *FireWatch India — FIRE ALERT*
━━━━━━━━━━━━━━━━━━

{emoji} *Fire Type:* {fire_type}
⚠️ *Priority:* {priority}

📍 *Location:* {lat:.3f}°N, {lon:.3f}°E
⚡ *FRP:* {frp} MW
🎯 *Confidence:* {confidence}%
📅 *Detected:* {date}

━━━━━━━━━━━━━━━━━━
🛰 *Source:* NASA FIRMS VIIRS
🤖 *System:* FireWatch India — SIH 2026
        """

        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        payload = {
            "chat_id": CHAT_ID,
            "text": message,
            "parse_mode": "Markdown"
        }

        response = requests.post(url, json=payload, timeout=10)
        if response.status_code == 200:
            print(f"Telegram alert sent — {fire_type}")
        else:
            print(f"Telegram error: {response.text}")

    except Exception as e:
        print(f"Alert error: {e}")


def send_summary_alert(total, industrial, wildfire, agricultural, gas_flare, date):
    """Send summary alert after fetch"""
    try:
        message = f"""
🛰 *FireWatch India — Fetch Complete*
━━━━━━━━━━━━━━━━━━

📅 *Date:* {date}
📊 *Total Hotspots:* {total}

🏭 Industrial Fires: {industrial}
🌲 Wildfires: {wildfire}
🌾 Agricultural Burning: {agricultural}
🔥 Gas Flares: {gas_flare}

━━━━━━━━━━━━━━━━━━
🤖 FireWatch India — SIH 2026
        """

        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        payload = {
            "chat_id": CHAT_ID,
            "text": message,
            "parse_mode": "Markdown"
        }

        requests.post(url, json=payload, timeout=10)
        print("Summary alert sent")

    except Exception as e:
        print(f"Summary alert error: {e}")