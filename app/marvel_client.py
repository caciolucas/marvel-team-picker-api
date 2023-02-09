import requests
from datetime import datetime
from hashlib import md5


class MarvelAPIClient:
    def __init__(self, base_url, private_key, public_key):
        self.base_url = base_url
        self.private_key = private_key
        self.public_key = public_key

    def generate_hash(self) -> tuple[int, str]:
        """
        Generate the timestamp and hash for the Marvel API request
        """

        ts = int(datetime.now().timestamp())
        hash_string = f'{ts}{self.private_key}{self.public_key}'
        return ts, md5(hash_string.encode('utf-8')).hexdigest()

    def make_request(self, method, endpoint, params=None):
        """
        Make a request to the Marvel API specific endpoint with the given params
        """
        try:
            ts, hash = self.generate_hash()
            url = f'{self.base_url}/{endpoint}?ts={ts}&apikey={self.public_key}&hash={hash}'
            response = requests.request(method, url, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as error:
            print(f'Error making request to Marvel API: {error}')
            return None

    def get_characters(self, name=None, limit=100, offset=0, **kwargs):
        """
        Get a list of characters from the Marvel API
        """
        params = {
            'name': name,
            'limit': limit,
            'offset': offset
        }
        return self.make_request('GET', 'characters', params)
