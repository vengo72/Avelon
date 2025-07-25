import os.path
from googleapiclient.discovery import build
import googleapiclient.discovery
from google.oauth2 import service_account
from googleapiclient.errors import HttpError


SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SERVICE_FILE = os.path.join(BASE_DIR, "credations.json")

credentials = service_account.Credentials.from_service_account_file(SERVICE_FILE, scopes=SCOPES)

# The ID and range of a sample spreadsheet.
SAMPLE_SPREADSHEET_ID = '1g2GzJUsR6lqNPdHCjiWK4s8MIirUGPxwTdQytR4IwRM'
SAMPLE_RANGE_NAME = 'Data'


def data():
    try:
        service = build('sheets', 'v4', credentials=credentials)

        # Call the Sheets API
        sheet = service.spreadsheets()
        result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                    range=SAMPLE_RANGE_NAME).execute()
        values = result.get('values', [])

        if not values:
            print('No data found.')
            return

        print('строка:', end=' ')
        for row in values:
            # Print columns A and E, which correspond to indices 0 and 4.
            print(' '.join(row))
    except HttpError as err:
        print(err)


if __name__ == '__main__':
    data()

