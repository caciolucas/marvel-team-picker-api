from sqlalchemy import Boolean, Column, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy import Table, Column, ForeignKey

import uuid
from app.database import Base

team_participants = Table(
    'team_participants', Base.metadata,
    Column('character_id', UUID(as_uuid=True), ForeignKey('characters.id')),
    Column('team_id', UUID(as_uuid=True), ForeignKey('teams.id'))
)


class Character(Base):
    __tablename__ = "characters"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    name = Column(String, unique=False)
    description = Column(String)
    thumbnail = Column(String)
    is_avenger = Column(Boolean, default=False)
    teams = relationship("Team", secondary=team_participants)


class Team(Base):
    __tablename__ = "teams"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    name = Column(String, unique=False)
    description = Column(String)
    characters = relationship("Character", secondary=team_participants)

