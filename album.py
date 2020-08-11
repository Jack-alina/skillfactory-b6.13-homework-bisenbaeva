import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

DB_PATH = "sqlite:///albums.sqlite3"
Base = declarative_base()

class Album(Base):
	__tablename__ = "album"

	id = sa.Column(sa.Integer, primary_key=True)
	year = sa.Column(sa.Integer)
	artist = sa.Column(sa.Text)
	genre = sa.Column(sa.Text)
	album = sa.Column(sa.Text)

def connect_db():
    engine = sa.create_engine(DB_PATH)
    Base.metadata.create_all(engine)
    session = sessionmaker(engine)
    return session()

# Нахадим все альбомы artist
def find(artist):
    session = connect_db()
    albums = session.query(Album).filter(Album.artist == artist).all()
    return albums

# Считаем количество альбомов artist
def album_counter(artist):
    session = connect_db()
    album_count = session.query(Album).filter(Album.artist == artist).count()
    return album_count

# Добавляем новый альбом в базу данных
def add_album(year, artist, genre, album):
    session = connect_db()
    album_names = [album.album for album in find(artist)]
    new_album = Album(year=year, artist=artist, genre=genre, album=album)

    if new_album.album in album_names:
        return True
    else: 
        session.add(new_album)
        session.commit() 

