import requests
import pandas as pd
import os
from flight_data import FlightData
from requests.auth import HTTPBasicAuth


class DataManager:
    # This class is responsible for talking to the Google Sheet.
    def __init__(self):
        """
        Initialize connection with Sheety API
        """
        self._endpoint = 'https://api.sheety.co/ba76a5bf33ef1b49693377356ed73055/flightDeals/prices'
        self._user = os.environ['ENV_SHEETY_USR']
        self._password = os.environ['ENV_SHEETY_PWD']
        self._authorization = HTTPBasicAuth(self._user, self._password)
        self.flights_data = self._get_sheet_data()


    def add_city(self, city, IATA, price):
        """
        Adds a new city to the spreadsheet using the Sheety API.
        If city exists, add missing information :).

        :param city: City's name
        :param IATA: City's IATA code
        :param price: Maximum flight price
        :return: None
        """
        row_id = 0  # Id of the row to be modified.

        # Update local data
        new_row = [city, IATA, price] # New row to be added or renewed
        if city in self.flights_data['city'].values:
            city_data = self.flights_data[self.flights_data['city'] == city]
            row_id = city_data.index[0]
        # Create a new entry
        else:
            row_id = self.flights_data.shape[0] + 2
        # Update dataframe
        self.flights_data.loc[row_id] = new_row

        # Update Spreadsheet
        # Request endpoint (specify row to be changed)
        url = self._endpoint + '/' + str(row_id)
        # Request body
        body = {
            'price':
                {
                    'city': city,
                    'iataCode': IATA,
                    'lowestPrice': price
                }
        }
        # Send PUT request so rows with missing data will be updated
        _ = requests.put(url=url, json=body, auth=self._authorization)


    def _get_sheet_data(self):
        """
        Returns the current state of the Google Sheet.

        :return: DataFrame containing the current state of the spreadsheet
        """
        response = requests.get(url=self._endpoint, auth=self._authorization)
        response_json = response.json()
        data = pd.DataFrame(response_json['prices']).set_index('id')
        print(data)
        return data


    def remove_city(self, city):
        """
        Removes a city from the spreadsheet using Sheety API.

        :param city:
        :return:
        """

        pass


if __name__ == '__main__':
    data_manager = DataManager()
    flight_manager = FlightData()
    city = 'Paris'
    iata_code = flight_manager.get_iata_code(city)
    data_manager.add_city(city, iata_code, 5000)
