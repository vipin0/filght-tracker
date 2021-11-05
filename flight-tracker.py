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
from utils.icao_code import get_airport_detail

class FlightTracker(DateTimeConversion):
    """This class provide all the functionalities for the FlightTracker.
    """
    
    def __init__(self) -> None:
        self.BASE_URL = "https://opensky-network.org/api"


    def __get_flights(self,query_type,airport,begin:datetime,end:datetime):
        """This method gets all the flights for the given query and time interval.
        """
        begin = self.datetime_to_unix(begin)
        end = self.datetime_to_unix(end)
        url = f"{self.BASE_URL}/flights/{query_type}?airport={airport}&begin={begin}&end={end}"
        
        try:
            response = requests.get(url)
        except ConnectionError:
            print("Connection Error!! Please check you connection.",file=sys.stderr)
            sys.exit(1)
        except Exception:
            print("Something went wrong!!",file=sys.stderr)
            sys.exit(1)

        result = response.json()
        time_var = "lastSeen"
        if query_type == "departure":
            time_var = "firstSeen"
        flightdetails = [[f["icao24"],f["estDepartureAirport"],f["estArrivalAirport"],self.unix_to_datetime(f[time_var])]
                             for f in result if f["estDepartureAirport"] and f["estArrivalAirport"]]
        return flightdetails

    def get_arrivals(self,airport,begin=datetime.now()-timedelta(7),end=datetime.now()):
        """This method gets all the arriving flights for the given query and time
         interval by calling get_flights() method.
        """
        flightdetails = [["Flight No.","Departed From","Coming to","ETA"]]

        flightdetails += self.__get_flights("arrival",airport=airport,begin=begin,end=end)
        
        return flightdetails

    def get_departures(self,airport,begin=datetime.now()-timedelta(7),end=datetime.now()):
        """This method gets all the departing flights for the given query and time 
        interval by calling get_flights() method.
        """
        flightdetails = [["Flight No.","Departed From","Going To","ETD"]]
        flightdetails += self.__get_flights("departure",airport=airport,begin=begin,end=end)
        return flightdetails

    def print_flights(self,flightdetails,ap_detail):
        """This method gets print all the flights in the table format.
        """
        print("*"*65)
        print("Flight Details".center(65),end="\n\n")
        print(ap_detail.center(65),end="\n")
        print("*"*65)
        print("\n",tabulate(flightdetails,headers="firstrow"))



############################# main handler function ###################################

def handle_arrival_depart_call(function_name,icaocode,begin,end):
    """This is the main handler function which accept a function_name
        will be called using the other arguments.

    """

    result = None
    if begin and end:
        if end - begin > timedelta(7):
            print("Time interval must be less than 7 days.",file=sys.stderr)
            sys.exit(1)
        result = function_name(icaocode,begin,end)
    elif begin:
        end = begin+timedelta(7)
        result = function_name(icaocode,begin=begin,end=end)
    elif end:
        begin = end-timedelta(7)
        result = function_name(icaocode,begin=begin,end=end)
    else:
        result = function_name(icaocode)
    # f.print_flights(result,ap_detail)
    return result

########################################################################################


@click.command()
@click.argument("airport_name_or_city_name")
@click.option('-a', '--arrival',is_flag=True,help="list the arriving airplanes to the given airport.")
@click.option('-d', '--depart',is_flag=True,help="list the depaturting airplanes from the given airport.")
@click.option('-b', '--begin',type=click.DateTime(formats=["%Y-%m-%d %H:%M:%S"])
            ,help="starting time in Y-m-d H:M:S")
@click.option('-e', '--end',type=click.DateTime(formats=["%Y-%m-%d %H:%M:%S"]),
            help="ending time in Y-m-d H:M:S")

def main(airport_name_or_city_name,arrival,depart,begin,end):
    """main method of the script."""
    # print(f"{arrival}\n{depart}\n{begin}\n{end}")

    if not arrival and not depart:
        arrival=True

    icaocode,ap_detail = get_airport_detail(airport_name_or_city_name)
    
    f = FlightTracker()
    
    if arrival:
        result = handle_arrival_depart_call(f.get_arrivals,icaocode,begin,end)
        f.print_flights(result,ap_detail)
    elif depart:
        result = handle_arrival_depart_call(f.get_departures,icaocode,begin,end)
        f.print_flights(result,ap_detail)

if __name__ == "__main__":
    main()
