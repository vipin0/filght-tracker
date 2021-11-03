import json
FILE_NAME = "utils/airports.json"


def get_airport_detail(query:str):
    # print(query)
    result = []
    airports_data = json.loads(open(FILE_NAME).read())
    for data in airports_data:
        # print(data)
        if query.lower() in data["name"].lower() or query.lower() in data["city"].lower():
            result.append(data)
    return result

