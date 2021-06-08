# For get_current_time
from urllib import request, error
from datetime import datetime, timedelta 

def get_current_time():
    str_time = request.urlopen('https://www.naver.com').headers['Date']
    current_time = datetime.strptime(str_time,'%a, %d %b %Y %H:%M:%S %Z') - timedelta(hours=-9) 
    return current_time.strftime("%Y-%m-%d %H:%M:%S")

def calculate_elapsed(start_time, end_time):
    start_time = datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S")
    end_time = datetime.strptime(end_time, "%Y-%m-%d %H:%M:%S")

    return end_time - start_time

def handle_timedelta(td):
    days = td.days
    hours = td.seconds//3600
    minutes = (td.seconds//60)%60
    seconds = td.seconds % 60
    return_string = ''
    if days != 0:
        return_string += f'{days}일 '
    if hours != 0:
        return_string += f'{hours}시간 '
    if minutes != 0:
        return_string += f'{minutes}분 '
    if seconds != 0:
        return_string += f'{seconds}초'

    return return_string