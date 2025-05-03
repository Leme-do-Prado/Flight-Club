import requests
from flight_data import FlightData

AMADEUS_API_ID = ""
AMADEUS_API_TOKEN = ""

class FlightSearch:
    def __init__(self):
        self.client_id = AMADEUS_API_ID
        self.client_secret = AMADEUS_API_TOKEN
        self.amadeus_token = self.get_access_token()

    def get_access_token(self):
        url = "https://test.api.amadeus.com/v1/security/oauth2/token"
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        data = {
            "grant_type": "client_credentials",
            "client_id": self.client_id,
            "client_secret": self.client_secret
        }
        response = requests.post(url, headers=headers, data=data)
        response.raise_for_status()
        return response.json()["access_token"]

    def get_destination_code(self, city_name):
        url = "https://test.api.amadeus.com/v1/reference-data/locations"
        headers = {"Authorization": f"Bearer {self.amadeus_token}"}
        params = {
            "keyword": city_name,
            "subType": "CITY"
        }
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        return response.json()["data"][0]["iataCode"]

    def get_flight_data(self, origin_city_code, destination_city_code, from_date, to_date):
        url = "https://test.api.amadeus.com/v2/shopping/flight-offers"
        headers = {
            "Authorization": f"Bearer {self.amadeus_token}"
        }
        params = {
            "originLocationCode": origin_city_code,
            "destinationLocationCode": destination_city_code,
            "departureDate": from_date,
            "returnDate": to_date,
            "adults": 1,
            "max": 1,
            "currencyCode": "USD"
        }
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()

        data = response.json()["data"][0]
        itinerary = data["itineraries"][0]["segments"][0]

        price = float(data["price"]["total"])

        try:
            return_date = data["itineraries"][1]["segments"][0]["departure"]["at"].split("T")[0]
        except IndexError:
            return_date = itinerary["departure"]["at"].split("T")[0]

        return FlightData(
            price=price,
            origin_city=origin_city_code,
            origin_airport=itinerary["departure"]["iataCode"],
            destination_city=destination_city_code,
            destination_airport=itinerary["arrival"]["iataCode"],
            out_date=itinerary["departure"]["at"].split("T")[0],
            return_date=return_date
        )


