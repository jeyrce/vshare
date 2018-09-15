# coding = utf-8
# env    = python3.5.2
# author = lujianxin
# time   = 2018-04-20
# purpose= 获得格式化当前时间

import time

def now():
    now_ = time.strftime('%Y-%m-%d %H:%M:%S')
    return now_
def date_time():
    return time.strftime('%Y-%m-%d')
def time_time():
    return time.strftime('%H:%M:%S')
def this_year():
    return time.strftime('%Y')
def this_month():
    return time.strftime('%m')
def this_day():
    return time.strftime('%d')
def this_hour():
    return time.strftime('%H')
def this_minute():
    return time.strftime('%M')
def this_second():
    return time.strftime('%S')

if __name__ == '__main__':
    print(now(), type(now()))
    pass

