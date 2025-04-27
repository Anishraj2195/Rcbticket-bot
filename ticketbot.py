import requests
from bs4 import BeautifulSoup
from telegram import Bot
import time

# Your Telegram bot details
BOT_TOKEN = '7221550596:AAH8HAkl-Gb_Occ96jZLXdovuoADULeMxQ8'
CHAT_ID = '5231089192'

# Create a Bot instance
bot = Bot(token=BOT_TOKEN)

# Track the previous ticket status
last_status = None

def check_for_csk_tickets():
    global last_status
    url = "https://shop.royalchallengers.com/ticket"
    headers = {"User-Agent": "Mozilla/5.0"}

    try:
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')

        # Look for the CSK match block
        matches = soup.find_all('div')

        csk_match_found = False
        for match in matches:
            text = match.get_text(separator=" ").strip()
            if "Royal Challengers Bengaluru" in text and "Chennai Super Kings" in text:
                csk_match_found = True
                text_upper = text.upper()

                # Determine the current status
                if any(keyword in text_upper for keyword in ["BUY TICKETS", "BOOK TICKETS", "BUY", "AVAILABLE"]):
                    current_status = "available"
                elif "COMING SOON" in text_upper or "PHASE 1 SOLD OUT" in text_upper or "SOLD OUT" in text_upper:
                    current_status = "sold out"
                else:
                    current_status = "unknown"

                # Only notify when status changes from 'sold out' or 'coming soon' to 'available'
                if last_status in ["sold out", "unknown", None] and current_status == "available":
                    message = f"🎟️ RCB vs CSK Tickets are now AVAILABLE! Hurry up and book!"
                    bot.send_message(chat_id=CHAT_ID, text=message)
                    print(f"Notification Sent: {message}")

                # Update the last_status
                last_status = current_status

                # Always print the current status in terminal
                print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] RCB vs CSK Tickets Status: {current_status.upper()}")
                break

        if not csk_match_found:
            print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] RCB vs CSK match not listed yet.")

    except Exception as e:
        print(f"Error checking tickets: {e}")

# Keep checking every 5 seconds
while True:
    check_for_csk_tickets()
    time.sleep(5)
