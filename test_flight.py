"""This is the test module to test all the 
functionalities of the project.
"""

from datetime import datetime
from utils.date import DateTimeConversion
from utils.flights import get_all_flights
from utils.icao_code import resolve_airport_detail,get_airport_detail

def test_date_conversion():
    """function to date time conversion functions.
    """
    d = DateTimeConversion()
    assert d.datetime_to_unix(datetime.strptime("2021-01-01 01:00:00","%Y-%m-%d %H:%M:%S")) == 1609462800
    assert d.unix_to_datetime(1609462800) == '2021-01-01 01:00:00'

def test_get_all_flights():
    """tests for get all fights function for paytm api
    """
    assert type(get_all_flights('lko','maa')) == str
    assert type(get_all_flights('lko','gjgh')) == str


def test_resolve_airport_detail():
    """testcases for resolve_airport_detail function
    """
    assert len(resolve_airport_detail('LKO')) == 6
    assert resolve_airport_detail('LKOKJ') == {}

def test_get_airport_detail():
    """testcases for get_airport_detail function
    """
    assert type(get_airport_detail('LKO')) == tuple
    assert get_airport_detail('LKHJ') == None

