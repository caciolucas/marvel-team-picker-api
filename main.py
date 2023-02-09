from typing import List

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware
from app import crud, models, schemas
from app.database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/characters")
def read_characters(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), name: str = None, is_avenger: bool = False) -> List[
    schemas.Character]:
    characters = crud.get_characters(db, skip=skip, limit=limit, name=name, is_avenger=is_avenger)
    return characters


@app.put("/characters/{character_id}")
def update_character(character_id: str, character: schemas.Character, db: Session = Depends(get_db)):
    db_character = crud.get_character(db, character_id)
    if db_character is None:
        raise HTTPException(status_code=404, detail="Character not found")
    db_character = crud.update_character(db, db_character, character)
    return db_character

@app.get("/teams")
def read_teams(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), name: str = None) -> List[
    schemas.Team]:
    if limit == -1:
        teams = crud.get_teams(db, skip=skip, name=name)
    else:
        teams = crud.get_teams(db, skip=skip, limit=limit, name=name)
    return teams

@app.delete("/teams/{team_id}/characters/{character_id}")
def delete_team_character(team_id: str, character_id: str, db: Session = Depends(get_db)):
    db_team = crud.get_team(db, team_id)
    if db_team is None:
        raise HTTPException(status_code=404, detail="Team not found")
    character = crud.get_character(db, character_id)
    if character is None:
        raise HTTPException(status_code=404, detail="Character not found")
    db_team = crud.delete_team_character(db, db_team, character)
    return db_team

@app.post("/teams/{team_id}/characters/")
def add_team_character(team_id: str, character_id: str, db: Session = Depends(get_db)):
    db_team = crud.get_team(db, team_id)
    if db_team is None:
        raise HTTPException(status_code=404, detail="Team not found")
    character = crud.get_character(db, character_id)
    if character is None:
        raise HTTPException(status_code=404, detail="Character not found")
    db_team = crud.add_team_character(db, db_team, character)
    return db_team
