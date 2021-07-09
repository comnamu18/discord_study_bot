from urllib import request
from datetime import datetime, timedelta


def get_current_time_object():
    str_time = request.urlopen("https://www.naver.com").headers["Date"]
    current_time = datetime.strptime(str_time, "%a, %d %b %Y %H:%M:%S %Z") - timedelta(hours=-9)

    return current_time


def calculate_elapsed_object(start_time, end_time):
    return end_time - start_time
