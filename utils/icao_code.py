"""This module help to resolve the ICAO code from the json file.

"""
import json
import sys

FILE_NAME = "utils/airports.json"


def resolve_airport_detail(query:str):
    """This method accept the query and return the icao code and airport detail.
    """
    # print(query)
    result = []
    airports_data = json.loads(open(FILE_NAME).read())
    for data in airports_data:
        # print(data)
        if query.lower() in data["name"].lower() or query.lower() in data["city"].lower():
            result.append(data)
    return result


def get_airport_detail(airport_name_or_city_name):
    """utility function to resolve airport detail"""
    details = resolve_airport_detail(airport_name_or_city_name)
    if len(details) == 0:
        print("No airport code found with given name. Try a finer search!!",file=sys.stderr)
        sys.exit(1)
    elif len(details) != 1:
        print("Multiple airport codes found with given name. Try a finer search!!",file=sys.stderr)
        sys.exit(1)
    else:
        icaocode = details[0]["icao"]
        name = details[0]["name"]
        city = details[0]["city"] 
        ap_detail = f"{name}, {city} - ICAO : {icaocode}"
    return (icaocode,ap_detail)

