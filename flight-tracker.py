"""This mudule provide functionlities to 
list arrival and departure information for 
any airport in the world.

"""

import click
import requests
from utils.date import DateTimeConversion
from datetime import datetime, timedelta
from tabulate import tabulate

class FlightTracker(DateTimeConversion):
    
    def __init__(self) -> None:
        self.BASE_URL = "https://opensky-network.org/api"

    def __get_flights(self,query_type,airport,begin=datetime.now()-timedelta(7),end=datetime.now()):
        begin = self.datetime_to_unix(begin)
        end = self.datetime_to_unix(end)
        url = f"{self.BASE_URL}/flights/{query_type}?airport={airport}&begin={begin}&end={end}"
        response = requests.get(url)
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
        print("\n\n",tabulate(flightdetails,headers="firstrow"))



f = FlightTracker()
res = f.get_arrivals("VILK")
f.print_flights(res)

# res = f.get_departures("VILK")
# f.print_flights(res)

# print(res)





# def get_arrivals():
#     pass

# @click.command()
# @click.argument("ICAO CODE")
# @click.option('-a', '--arival',is_flag=True,help="to list the arivals")
# @click.option('-d', '--depart',is_flag=True,help="to list the depatures")
# @click.option('-b', '--begin',type=str,help="starting time")
# @click.option('-e', '--end',is_flag=True,help="ending time")
# def main():
#     pass

# if __name__ == "__main__":
#     main()
