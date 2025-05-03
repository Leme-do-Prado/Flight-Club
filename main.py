from data_manager import DataManager
from flight_search import FlightSearch
from notification_manager import NotificationManager
from flight_data import FlightData
from datetime import datetime, timedelta

data_manager = DataManager()
flight_search = FlightSearch()
notification_manager = NotificationManager()

ORIGIN_CITY_IATA = "GRU"

sheet_data = data_manager.get_destination_data()

if sheet_data[0]["iataCode"] == "":
    for row in sheet_data:
        row["iataCode"] = flight_search.get_destination_code(row["city"])
    data_manager.destination_data = sheet_data
    data_manager.update_destination_codes()

tomorrow = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
six_months_later = (datetime.now() + timedelta(days=180)).strftime("%Y-%m-%d")

for destination in sheet_data:
    flight = flight_search.get_flight_data(
        ORIGIN_CITY_IATA,
        destination["iataCode"],
        from_date=tomorrow,
        to_date=six_months_later
    )

    if flight is None:
        continue

    if float(flight.price) < float(destination["lowestPrice"]):
        message = (
            f"Low price alert! Only ${flight.price} to fly from "
            f"{flight.origin_city}-{flight.origin_airport} to "
            f"{flight.destination_city}-{flight.destination_airport}, from "
            f"{flight.out_date} to {flight.return_date}."
        )
        notification_manager.send_sms(message)
