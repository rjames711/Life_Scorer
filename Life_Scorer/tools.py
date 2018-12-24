import datetime

def convert_timestamp(timestamp, offset):
    dt = datetime.datetime.utcfromtimestamp(timestamp/1000)
    dt = dt - datetime.timedelta(minutes=offset)
    date = dt.strftime('%Y-%m-%d')
    time = dt.strftime('%H:%M:%S')
    return date,time


def get_days(history_len):
    #TODO fix timezone hardcoding below
    dt = datetime.datetime.utcnow() -datetime.timedelta(hours=5)
    dates = []
    for days in range(history_len):
        offdt = dt - datetime.timedelta(days = days)
        date = str(offdt.date())
        dates.append(date)
    return dates

