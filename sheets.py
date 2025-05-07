import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd

# Define the scope and authenticate
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("creds.json", scope)
client = gspread.authorize(creds)

# Open the spreadsheet by URL
SPREADSHEET_URL = "https://docs.google.com/spreadsheets/d/1FT0TZ1WssMkMvXWxcF2EUWNyKzJjGwLNQeyaVAT3AhA/edit?usp=sharing"
sheet = client.open_by_url(SPREADSHEET_URL)
worksheet = sheet.sheet1

records = worksheet.get_all_records()
df = pd.DataFrame(records)

# Print the DataFrame
print(df)
