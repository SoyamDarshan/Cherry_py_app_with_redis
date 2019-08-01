import os
import csv
import redis_connection
from download_and_unzip import get_downloadable_links, download_file


def find_column_number(field_names):
    column_number_mapping = dict()
    read_csv = csv.reader(csvfile, delimiter=',')
    column_names = next(read_csv)
    for i in range(len(column_names)):
        if column_names[i].strip() in field_names:
            column_number_mapping[
                field_names[
                    column_names[i]].strip()] = i
    return column_number_mapping


try:
    download_zip_file = get_downloadable_links()
    csvfile = open(download_file(download_zip_file[0]), 'r')

    field_names = {'SC_CODE': 'code',
                   'SC_NAME': 'name',
                   'OPEN': 'open',
                   'HIGH': 'high',
                   'LOW': 'low',
                   'CLOSE': 'close'
                   }

    read_csv = csv.reader(csvfile, delimiter=',')
    column_numbers = find_column_number(field_names)
    print(column_numbers)
    data = next(read_csv)
    rc = redis_connection.redis_connect()
    rc.flushall()
    for data in read_csv:
        key_name = data[column_numbers['name']].strip()
        insert_data = {
            'code': data[column_numbers['code']].strip(),
            'name': data[column_numbers['name']].strip(),
            'open': data[column_numbers['open']].strip(),
            'high': data[column_numbers['high']].strip(),
            'low': data[column_numbers['low']].strip(),
            'close': data[column_numbers['close']].strip(),
        }
        redis_connection.insert_into_redis(rc, key_name, insert_data)
except Exception as e:
    print(e)
