# Flight Tracker


## Project Description
It is a command-line utility developed in python which list arrival and departure information for any airport in the world for the time interval of 7 days. This project uses [OpenSky REST API](https://opensky-network.org/apidoc/rest.html).


## Installation

1. Clone the repository and navigate to `flight-tracker` directory.
```
git clone https://github.com/vipin0/filght-tracker.git
```
  
2. Install the required dependencies.
```
pip install -r requirements.txt
```
## Usage

```
Usage: 

  $ python flight-tracker.py [OPTIONS] AIRPORT_NAME_OR_CITY_NAME

  Options:
    -a, --arrival                   list the arriving airplanes to the given
                                    airport.
    -d, --depart                    list the depaturting airplanes from the
                                    given airport.
    -b, --begin [%Y-%m-%d %H:%M:%S]
                                    starting time in Y-m-d H:M:S
    -e, --end [%Y-%m-%d %H:%M:%S]   ending time in Y-m-d H:M:S
    --help                          Show this message and exit.

```

## CLI Reference
  *By default the script show all the airplanes within the time interval of `7 days`.*

  ### Changeing time interval
    use -b/--begin or -e/--end for change time interval.

  ### Arrival
    use -a or --arrival flag to list all the arriving airplanes.

  ### Departure
    use -a or --arrival flag to list all the departing airplanes.


## Dependencies
This project is uses the following third-party dependencies.
```
requests
click
tabulate
```


## Sample outputs
 #### Arrivals
 <img src="images/arrival.PNG"/><br>
 
 #### Departures
 <img src="images/depart.PNG"/>
