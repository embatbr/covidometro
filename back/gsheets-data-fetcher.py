# -*- coding: utf-8 -*-

from oauth2client.service_account import ServiceAccountCredentials
import gspread
import pandas as pd


SCOPE = [
    'https://spreadsheets.google.com/feeds',
    'https://www.googleapis.com/auth/drive'
]

DEFAULT_CREDENTIALS = ServiceAccountCredentials.from_json_keyfile_name(
    'credentials/covidometro-info-78d047b1cb0b.json',
    SCOPE
)

SOURCE_GSHEETS_KEY = '1MWQE3s4ef6dxJosyqvsFaV4fDyElxnBUB6gMGvs3rEc'

DEFAULT_HEADER = [
    'Estado', 'Total de Casos', 'Suspeitos', 'Curados', 'Óbitos', 'Testes',
    'Novos Casos','Novos Óbitos'
]
NUM_COLUMNS = len(DEFAULT_HEADER)


def read_values(gsheet_key, credentials):
    client = gspread.authorize(credentials)

    sheet = client.open_by_key(gsheet_key)
    worksheet = sheet.sheet1

    cells = worksheet.range('B4:I31')
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
    data[0][0] = 'BRASIL'

    return pd.DataFrame(data, columns=DEFAULT_HEADER)


def generate_data_file(gsheet_key, credentials, filename):
    filepath = '{}.csv'.format(filename)

    dataframe = read_values_as_dataframe(gsheet_key, credentials)
    dataframe.to_csv(filepath, index=False)


if __name__ == '__main__':
    generate_data_file(SOURCE_GSHEETS_KEY, DEFAULT_CREDENTIALS, 'data')
