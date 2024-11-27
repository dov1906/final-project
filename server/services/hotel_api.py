
# hotel_api.py

import requests

MAKCORPS_API_KEY = "674661a07d3a82d995227011" 
MAKCORPS_BASE_URL = "https://api.makcorps.com"

def get_city_id(city_name= "New York"):
    """
    Fetch the city ID from MakCorps API using the city name.
    """
    url = f"{MAKCORPS_BASE_URL}/mapping"
    params = {"api_key": MAKCORPS_API_KEY, "name": city_name}

    try:
        response = requests.get(url, params=params)
        if response.status_code == 200:
            data = response.json()
            if data:
                return data[0]["document_id"]
            return None
        else:
            print(f"Error fetching city ID: {response.status_code}")
            return None
    except Exception as e:
        print(f"Error: {e}")
        return None


def fetch_hotels(city_id = "154999", checkin = "2024-12-10", checkout= "2024-12-15", pagination=0, currency="USD", rooms=1, adults=2, children=0):
    """
    Fetch hotel data for a specific city ID.
    """
    url = f"{MAKCORPS_BASE_URL}/city"
    params = {
        "api_key": MAKCORPS_API_KEY,
        "cityid": city_id,
        "pagination": pagination,
        "cur": currency,
        "rooms": rooms,
        "adults": adults,
        "children": children,
        "checkin": checkin,
        "checkout": checkout,
    }
    try:
        response = requests.get(url, params=params)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error fetching hotels: {response.status_code}")
            return []
    except Exception as e:
        print(f"Error: {e}")
        return []
