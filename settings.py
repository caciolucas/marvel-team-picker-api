from decouple import config


BASE_URL = config('BASE_URL', default='https://gateway.marvel.com:443/v1/public')
PRIVATE_API_KEY = config('PRIVATE_API_KEY')
PUBLIC_API_KEY = config('PUBLIC_API_KEY')