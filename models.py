from sqlalchemy import *
from sqlalchemy.orm import scoped_session, sessionmaker, relationship, backref
from sqlalchemy.ext.declarative import declarative_base
import os

database_url = os.environ.get("DATABASE_URL", "sqlite:///database.sqlite3")

engine = create_engine(database_url, convert_unicode=True)
db_session = scoped_session(sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
))

Base = declarative_base()
Base.query = db_session.query_property()

class Player(Base):
    __tablename__ = 'player'
    id = Column(Integer, primary_key=True)
    name = Column(String(32))

class Score(Base):
    __tablename__ = 'score'
    id = Column(Integer, primary_key=True)
    rule = Column(String(32))
    power = Column(Integer)
    weapon = Column(String(32))
    result = Column(String(32))
    player_id = Column(Integer, ForeignKey('player.id'))
    player = relationship(
        Player,
        backref=backref(
            'players',
            uselist=True,
            cascade='delete,all'
        )
    )

