import requests
import time
import os


class FlightData:
    """
    This class is responsible for getting data from Amadeus
    """

    def __init__(self):
        # API Keys
        self._api_key = os.environ['ENV_AMAD_KEY']
        self._api_secret = os.environ['ENV_AMAD_SEC']
        # Base URL
        self.api_base = "https://test.api.amadeus.com/v1"
        self._token = ''
        # Token
        self._validate_token()

    def _validate_token(self):

        token = ''
        exp_time = ''
        # Read current token and expiration time (s)
        with open('auth_token.txt') as f:
            a = f.readline()
            try:
                token, exp_time = a.split(',')
            except ValueError:
                pass
        # Renew token if it's not valid or if token does not exist
        if token == '' or int(exp_time) <= int(time.time()):
            print('Token expired')
            self._renew_token()
        else:
            self._token = token
            print('Token still active')

        return True

    def _save_token(self, token, expire_time):
        """
        Saves a new auth token to a txt file to use before expiration.

        :param token: New token to be saved
        :param expire_time: Expiration time in (s)
        :return: None
        """

        with open('auth_token.txt', 'w') as f:
            f.write(f'{token},{expire_time}')


    def _renew_token(self) -> None:
        """
        Gets a new auth token to use the Amadeus API.

        :return: None.
        """

        url = self.api_base + '/security/oauth2/token'
        # Header with content type
        header = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        # Body of the HTTPS request
        body = {
            'grant_type': 'client_credentials',
            'client_id': self._api_key,
            'client_secret': self._api_secret
        }

        response = requests.post(url=url, data=body, headers=header)
        response_json = response.json()
        # Update token
        self._token = response_json['access_token']
        expiration_time = int(time.time() + int(response_json['expires_in']))
        self._save_token(self._token, expiration_time)


    def get_iata_code(self, city: str):
        """
        Returns the IATA code of the given city using the Amadeus API.

        :param city: City's name
        :return: IATA code
        """

        # Validate token
        self._validate_token()

        url = self.api_base + '/reference-data/locations/cities'
        # Body
        body = {
            'keyword': city
        }
        # Header
        header = {
            'Authorization': 'Bearer ' + self._token
        }
        response = requests.get(url=url, headers=header, params=body)
        response_json = response.json()
        iata_code = response_json['data'][0]['iataCode']

        return iata_code

    def get_flight(self, departure_iata, destination_iata, date, budget):
        """
        Returns  the flights from a departure city to a destination city
        in a given date.

        :param departure_iata: IATA code of the departure city
        :param destination_iata: IATA code of the destination city
        :param date: Date of departure
        :param budget: Maximum price for a flight.
        :return: A list of flights for the scheduled date.
        """

        # Validate token
        self._validate_token()

        url = 'https://test.api.amadeus.com/v2/shopping/flight-offers'  # endpoint
        # Authorization header
        header = {
            'Authorization': 'Bearer ' + self._token
        }
        # Request body
        body = {
            'originLocationCode': departure_iata,
            'destinationLocationCode': destination_iata,
            'departureDate': date,
            'adults': 1,
            'currencyCode': 'MXN',
            'maxPrice': budget
        }

        response = requests.get(url=url, headers=header, params=body)  # Get request response
        print(response.status_code)
        if response.status_code == 400:
            return None
        response_json = response.json()
        return response_json['data']

