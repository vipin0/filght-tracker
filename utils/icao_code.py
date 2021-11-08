"""This module help to resolve the ICAO code from the json file.

"""
import json
from pathlib import Path

FILE_NAME = Path(__file__).parent/"airports.json"

def resolve_airport_detail(query:str):
    """This method accept the query and return the icao code and airport detail.
    """
    # print("query:",query)
    # print(FILE_NAME)
    result = []
    airports_data = json.loads(open(FILE_NAME).read())
    for data in airports_data:
        # print(data)
        if query.lower() == data["iata_code"].lower():
            result.append(data)
            # print(data)
            return data
    return {}


def get_airport_detail(airport_code):
    """utility function to resolve airport detail"""
    details = resolve_airport_detail(airport_code)
    # print(details)
    if details == {}:
        return None
    else:
        icaocode = details["icao_code"]
        name = details["name"]
        city = details["city"] 
        ap_detail = f"{name}, {city} - ICAO : {icaocode}"
        return (icaocode,ap_detail)

