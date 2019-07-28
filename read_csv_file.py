from zipfile import ZipFile
import glob
import os
import csv
import redis_connection


def find_column_number(field_names):
    column_number_mapping = dict()
    with open(file_name) as csvfile:
        read_csv = csv.reader(csvfile, delimiter=',')
        column_names = next(read_csv)
        for i in range(len(column_names)):
            if column_names[i].strip() in field_names:
                column_number_mapping[
                    field_names[
                        column_names[i]].strip()] = i
    return column_number_mapping


try:
    files_available = glob.glob('./extracted_files/*')
    # Get most recent file
    file_name = max(files_available, key=os.path.getctime)
    print(f'loading {file_name} into the DB')

    field_names = {'SC_CODE': 'code',
                   'SC_NAME': 'name',
                   'OPEN': 'open',
                   'HIGH': 'high',
                   'LOW': 'low',
                   'CLOSE': 'close'
                   }

    with open(file_name, 'r') as csvfile:
        read_csv = csv.reader(csvfile, delimiter=',')
        column_numbers = find_column_number(field_names)
        # print(column_numbers)
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
            # print(insert_data)

            redis_connection.insert_into_redis(rc, key_name, insert_data)
except:
    print('Nothing to display')
