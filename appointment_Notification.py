import pandas as pd
import requests
from datetime import datetime, date

# bot username: apt226bot

def format_timedelta(td):
    total_seconds = int(td.total_seconds())

    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60

    return f"{hours} hours {minutes} minutes"

# Telegram info
TOKEN = "8794816467:AAHA01In7gn9-H69G5V68LdK9DBqAB5hrjQ"
## CHAT_ID = "8662593057"

# Read appointments
apts_DF = pd.read_csv("ex.csv")

# Load Telegram users, read their chatIDs
users_DF = pd.read_csv("users.csv")

# Today's date
today = str(date.today())

# Current time
now = datetime.now()

# Filter today's appointments -> GET THE APTS WE'RE INTERESTED IN 
# We don't have to just do today's appointments
# We could easily get tomorrow's, or all of this week, etc etc
today_appts = apts_DF[apts_DF["date"] == today].copy()

# Combine date + time columns into full datetime
today_appts["appointment_datetime"] = pd.to_datetime(
    today_appts["date"] + " " + today_appts["time"]
)

# Compute the difference between time till and now
today_appts["time_till"] = (
    today_appts["appointment_datetime"] - now
)

# format time till s.t. it's nice
today_appts["time_till_str"] = today_appts["time_till"].apply(format_timedelta)

## IF there are any apts we want, send a text
if len(today_appts) > 0:

    # Build message
    message = "Hello, audrey here, here are your interesting appointments coming up!: \n"
    message += "Today's appointments:\n\n"

    for _, row in today_appts.iterrows():
        message += f"Appointment in {row['time_till_str']}"

    # Telegram endpoint
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"

    # Send to every user
    for _, user in users_DF.iterrows():

        chat_id = str(user["chatID"])

        response = requests.post(url, data={
            "chat_id": chat_id,
            "text": message
        })

        print(f"Sent to {user['name']}")
        print(response.json())

else:
    print("No appointments today.")