"""This mudule provide functionlities to 
list arrival and departure information for 
any airport in the world.

"""
import sys
import click
import requests
from datetime import datetime, timedelta
from tabulate import tabulate

from utils.date import DateTimeConversion

class FlightTracker(DateTimeConversion):
    """This class provide all the functionalities for the FlightTracker.
    """
    
    def __init__(self) -> None:
        self.BASE_URL = "https://opensky-network.org/api"

    def __get_flights(self,query_type,airport,begin:datetime,end:datetime):
        begin = self.datetime_to_unix(begin)
        end = self.datetime_to_unix(end)
        url = f"{self.BASE_URL}/flights/{query_type}?airport={airport}&begin={begin}&end={end}"
        response = requests.get(url)
        # print(response.status_code)
        # print(response.text)
        result = response.json()
        # print(result[0])
        time_var = "lastSeen"
        if query_type == "departure":
            time_var = "firstSeen"
        flightdetails = [[f["icao24"],f["estDepartureAirport"],f["estArrivalAirport"],self.unix_to_datetime(f[time_var])] for f in result]
        return flightdetails

    def get_arrivals(self,airport,begin=datetime.now()-timedelta(7),end=datetime.now()):
        flightdetails = [["Flight No.","Departed From","Coming to","ETA"]]

        flightdetails += self.__get_flights("arrival",airport=airport,begin=begin,end=end)
        
        return flightdetails

    def get_departures(self,airport,begin=datetime.now()-timedelta(7),end=datetime.now()):
        flightdetails = [["Flight No.","Departed From","Going To","ETD"]]
        flightdetails += self.__get_flights("departure",airport=airport,begin=begin,end=end)
        return flightdetails

    def print_flights(self,flightdetails):
        print("*"*65)
        print("Flight Details".center(65),end="\n")
        print("*"*65)
        print("\n\n",tabulate(flightdetails,headers="firstrow"))


@click.command()
@click.argument("ICAOCODE")
@click.option('-a', '--arrival',is_flag=True,help="list the arriving airplanes to the given airport.")
@click.option('-d', '--depart',is_flag=True,help="list the depaturting airplanes from the given airport.")
@click.option('-b', '--begin',type=click.DateTime(formats=["%Y-%m-%d %H:%M:%S"])
            ,help="starting time in Y-m-d H:M:S")
@click.option('-e', '--end',type=click.DateTime(formats=["%Y-%m-%d %H:%M:%S"]),
            help="ending time in Y-m-d H:M:S")

def main(icaocode,arrival,depart,begin,end):
    # print(f"{arrival}\n{depart}\n{begin}\n{end}")

    f = FlightTracker()
    if arrival:
        result = None
        if begin and end:
            if begin + timedelta(7) > end:
                print("Time interval must be less than 7 days.",file=sys.stderr)
                sys.exit(1)
            result = f.get_arrivals(icaocode,begin,end)
        elif begin:
            end = begin+timedelta(7)
            result = f.get_arrivals(icaocode,begin=begin,end=end)
        elif end:
            begin = end-timedelta(7)
            result = f.get_arrivals(icaocode,begin=begin,end=end)
        else:
            result = f.get_arrivals(icaocode)
        f.print_flights(result)
    
    elif depart:
        result = None
        if begin and end:
            if begin + timedelta(7) > end:
                print("Time interval must be less than 7 days.",file=sys.stderr)
                sys.exit(1)
            result = f.get_departures(icaocode,begin,end)
        elif begin:
            end = begin+timedelta(7)
            result = f.get_departures(icaocode,begin=begin,end=end)
        elif end:
            begin = end-timedelta(7)
            result = f.get_departures(icaocode,begin=begin,end=end)
        else:
            result = f.get_departures(icaocode)
        f.print_flights(result)

if __name__ == "__main__":
    main()
