from sqlalchemy.orm import Session
from typing import Optional

from backend.database import SessionLocal
from backend.models import Album, Music

def is_mp3_file(filename: str) -> bool:
    """
    Function to check whether the uploaded file is .mp3 or not. 
    Checking by validating the file extension

    Parameters:
    - filename (str): The name of the file.

    Returns:
    - bool: True if the file has a .mp3 extension, False otherwise.
    """
    return filename.lower().endswith('.mp3')

def get_or_create_album(db: Session, album_title: str) -> Album:
    """
    This method is responsible for creating a new album in the database. 
    The album table is linked to the music field by foreign key.
    takes album title as a parameter
    if the title is already present in the database it returns the particular existing Album
    else it creates a new raw and returns that Album

    Parameters:
    - db (Session): The database session.
    - album_title (str): The title of the album.

    Returns:
    - Album: The existing or newly created Album instance.
    """
    existing_album = db.query(Album).filter(Album.title == album_title).first()
    if existing_album:
        return existing_album
    else:
        new_album = Album(title=album_title)
        db.add(new_album)
        db.commit()
        db.refresh(new_album)
        return new_album

def save_music_details(db: Session, title: str, artist: str, album_title: str, release_year: Optional[int], mp3_file: str) -> None:
    """
    Save music details to the database.
    if the album title is not none it calls the get_or_create_album method to create or get the album. 
    Then create a new entry in the database

    Parameters:
    - db (Session): The database session.
    - title (str): The title of the music.
    - artist (str): The artist of the music.
    - album_title (str): The title of the album (can be None if no album is specified).
    - release_year (Optional[int]): The release year of the music (can be None).
    - mp3_file (str): The filename of the MP3 file.

    Returns:
    - None
    """
    if album_title is not None:
        album_db = get_or_create_album(db, album_title)
        album_id = album_db.id
    else:
        album_id = None

    new_music = Music(title=title, artist=artist, album_id=album_id, release_year=release_year, mp3_file=mp3_file)
    db.add(new_music)
    db.commit()
    db.refresh(new_music)
