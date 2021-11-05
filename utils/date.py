"""This module convert time to unix timestamp and vice-versa.

"""
import time
from datetime import datetime

class DateTimeConversion:
    """This class provice functionalities for converting 
    datetime to unix timestamp and vice-versa.
    
    """
    def __init__(self) -> None:
        pass
    def unix_to_datetime(self,seconds):
        """This method unix timestamp to date time.
        """
        return datetime.utcfromtimestamp(int(seconds)).strftime('%Y-%m-%d %H:%M:%S')

    def datetime_to_unix(self,date_time:datetime):
        """This method convert datetime to unix timestamp.
        """
        return int(time.mktime(date_time.timetuple()))