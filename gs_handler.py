from googleapiclient.discovery import build
from google.oauth2 import service_account
import usd_rate as usd


SERVICE_ACCOUNT_FILE = 'keys.json'
# If modifying these scopes, delete the file keys.json.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

creds = None
creds = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)

# Spreadsheet ID
SAMPLE_SPREADSHEET_ID = '1Zi1kAqzpdfh65ji4i_ZcDwsRzL0dcz0qEjtNbFfoFCI'

service = build('sheets', 'v4', credentials=creds)

# Call the Sheets API
sheet = service.spreadsheets()

# Get all data from A2 to the last row in column D
def fetch_all_data(usd_rate):
        result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID, range="Sheet1!A2:D").execute()
        values = result.get('values')
        for row in values:
                row.insert(3, round(float(row[2])*usd_rate,2))
        return tuple(tuple(x) for x in values)













