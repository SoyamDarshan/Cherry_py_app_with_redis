import os
import operator
import redis

redis_host = "localhost"
redis_port = 6379
redis_password = ""
db = 0


def redis_connect():
    try:
        connect = redis.from_url(os.environ.get(
            "REDIS_URL"), db=1, decode_responses=True)

        return connect
    except Exception as e:
        print(e)


def insert_into_redis(rc, key_name, data):
    rc.hmset(key_name, data)
    # print('Inserted')
    return


def get_stock_value(name):
    rc = redis_connect()

    final_value = rc.hgetall(name.upper())
    final_value['profit'] = f'{calculate_percentage(final_value["open"], final_value["close"]): .2f}'

    return final_value


def calculate_percentage(open_value, close_value):
    return (((float(close_value))-float(open_value))/float(open_value))*100


def get_top_10_stocks():
    rc = redis_connect()
    top_10_values = dict()
    keys = rc.keys('*')
    final_value = []

    for value in keys:
        open_value = rc.hgetall(value)['open']
        close_value = rc.hgetall(value)['close']
        top_10_values[rc.hgetall(value)['name']] = calculate_percentage(
            open_value, close_value)

    top_10_values = sorted(top_10_values.items(),
                           key=operator.itemgetter(1), reverse=True)[:10]
    for value in top_10_values:
        final_value.append((f'{value[1]:.2f}', rc.hgetall(value[0])))

    return final_value


if __name__ == '__main__':
    get_top_10_stocks()
