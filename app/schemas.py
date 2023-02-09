from pydantic import BaseModel, UUID4
from typing import List


class CharacterBase(BaseModel):
    name: str
    description: str
    thumbnail: str
    is_avenger: bool = False
    teams: List[UUID4] = []


class CharacterCreate(CharacterBase):
    pass


class Character(CharacterBase):
    id: UUID4


class TeamBase(BaseModel):
    name: str
    description: str
    characters: List[UUID4] = []


class TeamCreate(TeamBase):
    pass


class Team(TeamBase):
    id: UUID4
    characters: List[Character] = []
