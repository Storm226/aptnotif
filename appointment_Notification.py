import pandas as pd
import requests
from datetime import date


# bot username: apt226bot

# Telegram info
TOKEN = "8794816467:AAHA01In7gn9-H69G5V68LdK9DBqAB5hrjQ"
CHAT_ID = "8662593057"

# Read appointments
df = pd.read_csv("ex.csv")

# Load Telegram users
users_df = pd.read_csv("users.csv")

print(users_df.columns)

# Today's date
today = str(date.today())

# Filter today's appointments
today_appts = df[df["date"] == today]

if len(today_appts) > 0:

    # Build message
    message = "Today's appointments:\n\n"

    for _, row in today_appts.iterrows():
        message += f"• {row['name']} — {row['time']}\n"

    # Telegram endpoint
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"

    # Send to every user
    for _, user in users_df.iterrows():

        chat_id = str(user["chatID"])

        response = requests.post(url, data={
            "chat_id": chat_id,
            "text": message
        })

        print(f"Sent to {user['name']}")
        print(response.json())

else:
    print("No appointments today.")