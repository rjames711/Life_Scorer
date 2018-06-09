import datetime

def convert_timestamp(timestamp, offset):
    dt = datetime.datetime.utcfromtimestamp(timestamp/1000)
    dt = dt - datetime.timedelta(minutes=offset)
    date = dt.strftime('%Y-%m-%d')
    time = dt.strftime('%H:%M:%S')
    return date,time

