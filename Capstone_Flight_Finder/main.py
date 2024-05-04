from data_manager import DataManager
from flight_data import FlightData
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
        if flight_price <= budget:
            cheaper_flights.append(flight_price)

    return cheaper_flights


if __name__ == '__main__':
    # Data Manager is responsible to manage the Google Sheet
    sheet = DataManager()
    flight_manager = FlightData()
    date = datetime.today().strftime('%Y-%m-%d')

    cheap_flights = {}
    # Iterate through each row in sheet's data
    for _, city in sheet.flights_data.iterrows():
        cheap_flights[city['city']] = get_cheaper_flights(
            flight_manager, 'MEX', city['iataCode'], date, city['lowestPrice'])

    print(cheap_flights)
