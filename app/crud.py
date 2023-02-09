from http.client import HTTPException

from sqlalchemy.orm import Session
from typing import List
from app import models, schemas


def get_character(db: Session, character_id: int) -> models.Character:
    character = db.query(models.Character).filter(models.Character.id == character_id).first()
    return character


def get_characters(db: Session, skip: int = 0, limit: int = 100, name: str = None, is_avenger: bool = False) -> List[
    schemas.Character]:
    queryset = db.query(models.Character).order_by(models.Character.name.asc()).filter_by(is_avenger=is_avenger)
    if name:
        queryset = queryset.filter(models.Character.name.ilike('%{}%'.format(name)))
    queryset = queryset.offset(skip).limit(limit).all()
    # Convert to list of schemas.Character
    characters = [schemas.Character(**character.__dict__) for character in queryset]
    return characters


def create_character(db: Session, character: schemas.CharacterCreate):
    db_character = models.Character(description=character.description)
    db.add(db_character)
    db.commit()
    db.refresh(db_character)
    character = schemas.Character(**db_character.__dict__)
    return character


def bulk_create_characters(db: Session, characters: List[schemas.CharacterCreate]):
    db_characters = [
        models.Character(name=character.name, description=character.description, thumbnail=character.thumbnail) for
        character in characters
    ]
    db.add_all(db_characters)
    db.commit()
    characters = [schemas.Character(**character.__dict__) for character in db_characters]
    return characters


def update_character(db: Session, character: models.Character, character_update: schemas.Character):
    character.name = character_update.name
    character.description = character_update.description
    character.thumbnail = character_update.thumbnail
    character.is_avenger = character_update.is_avenger
    character.teams = character_update.teams
    db.commit()
    db.refresh(character)
    return character


def create_team(db: Session, team: schemas.TeamCreate):
    db_team = models.Team(name=team.name, description=team.description)
    db.add(db_team)
    db.commit()
    db.refresh(db_team)
    return db_team


def add_team_character(db: Session, team: models.Team, character: models.Character):
    team.characters.append(character)
    db.commit()
    db.refresh(team)
    return team


def remove_team_character(db: Session, team: models.Team, character: models.Character):
    team.characters.remove(character)
    db.commit()
    db.refresh(team)
    return team


def get_team(db: Session, team_id: int):
    return db.query(models.Team).filter(models.Team.id == team_id).first()


def get_teams(db: Session, skip: int = 0, limit: int = 100, name: str = None) -> List[schemas.Team]:
    queryset = db.query(models.Team)
    if name:
        queryset = queryset.filter(models.Team.name.ilike('%{}%'.format(name)))
    # List comprehension to insert characters list into Team object
    teams = [schemas.Team(**team.__dict__,
                          characters=[schemas.Character(**character.__dict__) for character in team.characters])
             for team in queryset]
    return teams


def delete_team_character(db: Session, team: models.Team, character: models.Character):
    team.characters.remove(character)
    db.commit()
    db.refresh(team)
    return team
