from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker
from models import Player, Score, Base
import os

database_url = os.environ.get("DATABASE_URL", "sqlite:///database.sqlite3")
engine = create_engine(database_url, convert_unicode=True)
db_session = scoped_session(sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
))


def init_db():
    Base.metadata.create_all(bind=engine)
    player1 = Player(name="player1")
    db_session.add(player1)
    sc = Score(rule='ガチヤグラ', power=1900, weapon='スクリュースロッシャー', result='WIN', player=player1)
    db_session.add(sc)
    sc = Score(rule='ガチエリア', power=1920, weapon='スクリュースロッシャー', result='WIN', player=player1)
    db_session.add(sc)
    player2 = Player(name="player2")
    sc = Score(rule='ガチアサリ', power=2100, weapon='スプラシューター', result='WIN', player=player2)
    db_session.add(sc)
    sc = Score(rule='ガチエリア', power=2320, weapon='スプラシューターベッチュー', result='WIN', player=player2)
    db_session.add(sc)
    db_session.commit()

if __name__ == '__main__':
    init_db()