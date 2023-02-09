from app.marvel_client import MarvelAPIClient
from app import crud, schemas
from app.database import SessionLocal, engine

import settings
import json


def extract_characters():
    """ 
    To prevent the need to make multiple requests to the Marvel API,
    we can load all the characters at once and store them in a JSON file
    """
    client = MarvelAPIClient(settings.BASE_URL, settings.PRIVATE_API_KEY, settings.PUBLIC_API_KEY)
    characters = []
    response = client.get_characters()
    total = response['data']['total']
    while len(characters) < total:
        characters.extend(response['data']['results'])
        response = client.get_characters(offset=len(characters))

    with open('media/characters.json', 'w') as f:
        json.dump(characters, f)


def load_characters():
    """
    Load characters from JSON file into database
    """

    with open('media/characters.json', 'r') as f:
        characters_list = json.load(f)
    characters = [
        schemas.CharacterCreate(
            name=character['name'],
            description=character['description'],
            thumbnail=f'{character["thumbnail"]["path"]}.{character["thumbnail"]["extension"]}'
        ) for character in characters_list]

    db = SessionLocal()
    crud.bulk_create_characters(db, characters)
