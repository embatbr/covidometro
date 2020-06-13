# -*- coding: utf-8 -*-

import sys

from oauth2client.service_account import ServiceAccountCredentials
import gspread
import pandas as pd


DATA_DIR = 'data'

SCOPE = [
    'https://spreadsheets.google.com/feeds',
    'https://www.googleapis.com/auth/drive'
]

DEFAULT_CREDENTIALS = ServiceAccountCredentials.from_json_keyfile_name(
    'credentials/covidometro-info-78d047b1cb0b.json',
    SCOPE
)

SOURCE_GSHEETS_KEY = '1MWQE3s4ef6dxJosyqvsFaV4fDyElxnBUB6gMGvs3rEc'

NUM_COLUMNS = 8
DEFAULT_HEADER = [
    'Estado', 'Total de Casos', 'Suspeitos', 'Curados', 'Óbitos', 'Testes',
    'Novos Casos','Novos Óbitos'
]


def read_values(gsheet_key, credentials):
    client = gspread.authorize(credentials)

    sheet = client.open_by_key(gsheet_key)
    worksheet = sheet.sheet1

    cells = worksheet.range('B3:I31')
    values = list()
    cur_index = -1
    count = 0

    for cell in cells:
        if count % NUM_COLUMNS == 0:
            values.append(list())
            cur_index = cur_index + 1

        value = cell.value
        values[cur_index].append(value)

        count = count + 1

    return values


def read_values_as_dataframe(gsheet_key, credentials):
    data = read_values(gsheet_key, credentials)
    data.pop(0) # popping header

    data[0][0] = 'BRASIL'

    return pd.DataFrame(data, columns=DEFAULT_HEADER)


def generate_data_file(filename):
    filepath = '{}/{}.csv'.format(DATA_DIR, filename)

    dataframe = read_values_as_dataframe(SOURCE_GSHEETS_KEY, DEFAULT_CREDENTIALS)
    dataframe.to_csv(filepath, index=False)


if __name__ == '__main__':
    filename = sys.argv[1]
    generate_data_file(filename)
