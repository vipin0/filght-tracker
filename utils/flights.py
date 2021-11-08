"""This module provide all the basic utility function 
for the bot operations.

"""
import requests
from datetime import datetime
from tabulate import tabulate

from utils.icao_code import get_airport_detail
from flight_tracker import FlightTracker,handle_arrival_depart_call


def get_all_flights(org,dest,dept_date=datetime.today().strftime("%Y%m%d"),adults=1,class_='E'):
    """This method find all the available flights based on the query.
    
        This method uses paytm flight api for retrieving data.
    """
    if isinstance(dept_date,datetime):
        dept_date=dept_date.strftime("%Y%m%d")
    url = f"https://travel.paytm.com/api/flights/v2/search?adults={adults}&children=0&class={class_}&client=web&departureDate={dept_date}&origin={org}&infants=0&destination={dest}"
    # print(url)
    try:
        res = requests.get(url)
    except ConnectionError:
        print("Connection failed! Check your connection!")
    json_res = res.json()
    if json_res['code'] == 200:
        result = []
        flights = json_res["body"]["onwardflights"]['flights']
        if len(flights) == 0:
            return "No flights available."
    
        for f in flights:
            d = {
                'origin':f['origin'],
                'destination':f['destination'],
    #             'bookingClass':f['bookingClass']
                'airline':f['airline'],
                'departure':f"{f['departureDateAirport']} {f['departureTimeAirport']}",
                'arrival':f"{f['arrivalDateAirport']} {f['arrivalTimeAirport']}",
                'duration':f['duration'],
                'stops':len(f['hops']),
                'price':f['price'][0]['totalfare']
            }
            result.append(d)
        # showing only 10 flights
        return tabulate(result[:10],headers="keys")
    else:
        error = {
            'error':json_res['error'],
            'message':json_res['status']['message']['title']
        }
        return error['message']



def parse_query(query:list):
    """This function parses and validate the query for the search_flight command.
    
    """
    origin,dest,*optional_detail = query
    if len(optional_detail) == 0:
        return get_all_flights(origin,dest)

    if len(optional_detail)==1:
        try:
            print(optional_detail)
            travel_date = datetime.strptime(optional_detail[0],"%Y-%m-%d")
        except Exception as e:
            print(e)
            return "Invalid date!"
        return get_all_flights(origin,dest,travel_date)

    elif len(optional_detail) == 2:
        try:
            travel_date = datetime.strptime(optional_detail[0],"%Y-%m-%d")
        except Exception:
            return "Invalid date!"
        try:
            no_passengers = int(optional_detail[1])
        except Exception:
            return "Invalid number of passengers!"
        return get_all_flights(origin,dest,travel_date,no_passengers)
    
    elif len(optional_detail) == 3:
        try:
            travel_date = datetime.strptime(optional_detail[0],"%Y-%m-%d")
        except Exception:
            return "Invalid date!"
        try:
            no_passengers = int(optional_detail[1])
        except Exception:
            return "Invalid number of passengers!"
        class_ = optional_detail[2]
        if class_.upper() not in 'BE':
            return "Invalid class!"
        return get_all_flights(origin,dest,travel_date,no_passengers)


def parse_tracking_query(type,query:list):

    """This function parses and validate the query for the 
    list_arrivals and list_departures command.
    
    """

    airport,*time_detail = query
    ap = get_airport_detail(airport)
    if ap is None:
        return "No Airport is found for given IATA code."
    
    icaocode,ap_detail = ap
    
    f = FlightTracker()

    function_name = None
    if type == 'arrival':
        function_name = f.get_arrivals
    elif type == 'departure':
        function_name = f.get_departures

    if len(time_detail) == 0:
        result = handle_arrival_depart_call(function_name,icaocode)
        return pretty_print(result,ap_detail)

    if len(time_detail)==1:
        try:
            begin = datetime.strptime(time_detail[0],"%Y-%m-%d")
        except Exception:
            return "Invalid begin date! check date format."
        result = handle_arrival_depart_call(function_name,icaocode,begin=begin)
        return pretty_print(result,ap_detail)

    elif len(time_detail) == 2:
        try:
            begin = datetime.strptime(time_detail[0],"%Y-%m-%d")
        except Exception:
            return "Invalid begin date! check date format."
        try:
            end = datetime.strptime(time_detail[0],"%Y-%m-%d")
        except Exception:
            return "Invalid begin date! check date format."
        result = handle_arrival_depart_call(function_name,icaocode,begin=begin,end=end)
        return pretty_print(result,ap_detail)

def pretty_print(flightdetails,ap_detail):
    """This function print the details in nice manner.
    """
    # print(flightdetails,len(flightdetails))
    if len(flightdetails) >=2:
        # showing only 10 flights
        return f"""
            {"*"*65}\n
            {"Flight Details".center(65)}\n
            {ap_detail.center(65)}\n
            {"*"*65}\n
            {tabulate(flightdetails[:10],headers="firstrow")}
        """
    return f"""
            {"*"*65}\n
            {"Flight Details".center(65)}\n
            {ap_detail.center(65)}\n
            {"*"*65}\n\n
            {'No flights details found!!'.center(65)}
        """


    
        




    