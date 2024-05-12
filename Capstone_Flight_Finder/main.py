from data_manager import DataManager
from flight_data import FlightData
from notification_manager import NotificationManager
from datetime import datetime


def get_cheaper_flights(flight_data: FlightData, departure_iata, city_iata, date, budget):
    """
    This function explores a list of flights from a departure city to a
    destination city using Amadeus API. It returns a list of flights
    cheaper than the provided budget

    :param flight_data: A FlightData object to use Amadeus API.
    :param departure_iata: Departure city IATA code.
    :param city_iata: Destination city IATA code.
    :param date: Departure date in YYYY-MM-DD format.
    :param budget: Maximum flight price to search for.
    :return: The cheapest flight price.
    """

    cheaper_flights = []
    # Get a list of flights for the selected date
    flights = flight_data.get_flight(departure_iata, city_iata, date, budget)
    # If no flights found return empty list
    if not flights:
        return cheaper_flights

    # Inspect all flights
    for flight in flights:
        flight_price = flight['price']['total']
        if float(flight_price) <= float(budget):
            cheaper_flights.append(flight_price)

    return list(set(cheaper_flights))


def create_message(countries):

    msg = "Get ready for your next adventure! Here are some flights adjusted to your budget:"
    for country, flights in countries.items():
        # If no cheaper flights were found
        if not flights:
            continue
        # If found cheaper Flights
        msg += f"\n\n{country}: \n  * "
        msg += '\n  * '.join([str(price) for price in flights])

    return msg


def flights_available(flights: dict):
    """
    Check if there exists any flight available

    :param flights: Dictionary {country: [prices]}
    :return: True if there is at least one available flight. False otherwise
    """
    for _, prices in flights.items():
        if prices:
            return True

    return False


if __name__ == '__main__':
    # Data Manager is responsible to manage the Google Sheet
    sheet = DataManager()
    flight_manager = FlightData()
    sms_manager = NotificationManager()
    # date = datetime.today().strftime('%Y-%m-%d')
    date = '2024-05-14'
    cheap_flights = {}
    # Iterate through each row in sheet's data
    for _, city in sheet.flights_data.iterrows():
        cheap_flights[city['city']] = get_cheaper_flights(
            flight_manager, 'MEX', city['iataCode'], date, city['lowestPrice'])

    # If there are any available flights, send a message
    if flights_available(cheap_flights):
        print("Hay vuelos")
        sms_manager.send_msg(create_message(cheap_flights))

