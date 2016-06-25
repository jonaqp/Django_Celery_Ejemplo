import datetime


def str_datetime(format_default='%Y-%m-%d %H:%M:%S'):
    return datetime.datetime.now().strftime(format_default)


def str_date(format_default='%Y-%m-%d'):
    return datetime.datetime.now().strftime(format_default)


def str_time(format_default='%H:%M:%S'):
    return datetime.datetime.now().strftime(format_default)


def convert_str_in_date(date_report):
    convert_date = datetime.datetime.strptime(date_report, '%Y-%m-%d').date()
    return convert_date


def convert_str_in_datetime(date_report):
    convert_date = datetime.datetime.strptime(date_report, '%Y-%m-%d %H:%M:%S')
    return convert_date


def convert_unix_in_datetime(date_report):
    convert_date = datetime.datetime.fromtimestamp(int(date_report)).strftime('%Y-%m-%d %H:%M:%S')
    return convert_date


def convert_str_in_time(time_report):
    convert_time = datetime.datetime.strptime(time_report, '%H:%M:%S').time()
    return convert_time


def combine_date_with_time(date=datetime.datetime.today(), my_time='00:00:00'):
    if isinstance(my_time, str):
        my_time = convert_str_in_time(my_time)
    if isinstance(date, str):
        date = convert_str_in_date(date)
    my_datetime = datetime.datetime.combine(date, my_time)
    return my_datetime


def date_today():
    return datetime.date.today


def add_day(initial_date, num_days):
    return initial_date + datetime.timedelta(num_days)


def now_plus_1():
    return add_day(datetime.date.today(), 1)
