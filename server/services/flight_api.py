import requests
from config import FLIGHT_API_KEY

BASE_URL = "https://api.flightapi.io/roundtrip"

def get_flight_prices(
    departure_airport_code, 
    arrival_airport_code, 
    departure_date, 
    arrival_date, 
    number_of_adults, 
    number_of_childrens=0, 
    number_of_infants=0, 
    cabin_class="economy", 
    currency="USD", 
    region="US"
):
    """Fetch flight prices from FlightAPI."""
    try:
        # Construct the API URL
        url = f"{BASE_URL}/{FLIGHT_API_KEY}/{departure_airport_code}/{arrival_airport_code}/{departure_date}/{arrival_date}/{number_of_adults}/{number_of_childrens}/{number_of_infants}/{cabin_class}/{currency}/{region}"
        url = "https://api.flightapi.io/roundtrip/674630b2c3046da4eda9c232/JFK/SIN/2024-12-10/2024-12-15/1/0/0/Economy/USD"
        # Make the GET request
        response = requests.get(url)
        response.raise_for_status()  # Raise exception for HTTP errors

        # Parse the JSON response
        data = response.json()
        return data
    except requests.exceptions.RequestException as e:
        print(f"Error while fetching flight data: {e}")
        return None
