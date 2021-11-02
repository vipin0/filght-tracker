import click
import time
from datetime import datetime

class DateTimeConversion:

    def __init__(self) -> None:
        pass
    def unix_to_datetime(self,seconds):
        return datetime.utcfromtimestamp(int(seconds)).strftime('%Y-%m-%d %H:%M:%S')

    def datetime_to_unix(self,date_time:datetime):
        return int(time.mktime(date_time.timetuple()))