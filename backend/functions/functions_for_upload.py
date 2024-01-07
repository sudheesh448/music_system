from fastapi import HTTPException
import os
from sqlalchemy.orm import Session
from typing import Optional

from backend.database import SessionLocal
from backend.models import Album, Music

def is_mp3_file(filename: str) -> bool:

    """
    Function to check whether the uploaded file is .mp3 or not. 
    Checking by validating the file extension
    
    PARAMETERS:
    - filename (str): The name of the file.
    RETURNS:
    - bool: True if the file has a .mp3 extension, False otherwise.
    """
    try:
        return filename.lower().endswith('.mp3')
    
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")

def get_or_create_album(db: Session, album_title: str) -> Album:
    """
    This method is responsible for creating a new album in the database. 
    The album table is linked to the music field by foreign key.
    Takes album title as a parameter.
    If the title is already present in the database, it returns the particular existing Album.
    Else, it creates a new row and returns that Album.

    PARAMETERS:
        - album_title (str): The title of the album.

    RETURNS:
        - Album: The existing or newly created Album instance.
    """
    existing_album = db.query(Album).filter(Album.title == album_title).first()
    print("album")
    if existing_album:
        return existing_album
    else:
        print("here hdfk")
        new_album = Album(title=album_title)
        db.add(new_album)
        db.commit()
        return new_album
    
UPLOAD_FOLDER = 'uploads'
def save_music_details(db: Session, **kwargs) -> None:
    """
    Save music details to the database.
    If the album title is not None, it calls the get_or_create_album method to create or get the album.
    Then, create a new entry in the database.

    PARAMETERS:
        - title (str): The title of the music.
        - artist (str): The artist of the music.
        - album_title (str): The title of the album (can be None).
        - release_year (int): The release year of the music.
        - mp3_data: The MP3 data.

    RETURNS:
        - None
    """
    try:
        album_title = kwargs.get("album_title")
        if album_title is not None:
            album_db = get_or_create_album(db, album_title)
            album_id = album_db.id
        else:
            album_id = None

    mp3_file_name= kwargs.get("mp3_file_name")
    mp3_file_path = os.path.join(UPLOAD_FOLDER,mp3_file_name)
    mp3_data=kwargs.get("mp3_data")

    with open(mp3_file_path, 'wb') as mp3_file:
        mp3_file.write(mp3_data)

    new_music = Music(
        title=kwargs.get("title"),
        artist=kwargs.get("artist"),
        album_id=album_id,
        release_year=kwargs.get("release_year"),
        mp3_file_name=mp3_file_name,
        mp3_file_path=mp3_file_path,
    )
    db.add(new_music)
    db.commit()

    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")