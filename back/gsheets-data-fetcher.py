# -*- coding: utf-8 -*-

from oauth2client.service_account import ServiceAccountCredentials
import gspread
import pandas as pd


SCOPE = [
    'https://spreadsheets.google.com/feeds',
    'https://www.googleapis.com/auth/drive'
]

CREDENTIALS = ServiceAccountCredentials.from_json_keyfile_name(
    'credentials/covidometro-info-78d047b1cb0b.json',
    SCOPE
)


client = gspread.authorize(CREDENTIALS)
# print(dir(client))

worksheet = client.open_by_key('1MWQE3s4ef6dxJosyqvsFaV4fDyElxnBUB6gMGvs3rEc').sheet1
# worksheet = client.open_by_url(
#     'https://docs.google.com/spreadsheets/d/1MWQE3s4ef6dxJosyqvsFaV4fDyElxnBUB6gMGvs3rEc/edit?usp=sharing'
# ).sheet1

data = worksheet.get_all_values()
headers = data.pop(0)

df = pd.DataFrame(data, columns=headers)
print(df.head())