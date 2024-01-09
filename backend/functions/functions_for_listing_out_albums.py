from fastapi import HTTPException
from sqlalchemy.orm import Session
from backend.models import Album, Music
from typing import List, Dict

def get_all_albums(db: Session, page: int = 1, size: int = 10) -> List[Dict[str, any]]:
    """
    Get a list of all albums in the database.

    RETURNS:
        - List[dict]: List of dictionaries representing each album's details.
          Each dictionary has the following keys:
          - "album_id" (int): The unique identifier of the album.
          - "title" (str): The title of the album.
          - "favorite" (bool): Indicates whether the album is marked as a favorite.
    """

    try:
        offset = (page - 1) * size
        albums = db.query(Album).offset(offset).limit(size).all()

        result = []
        for album in albums:
            album_details = {
                "album_id": album.id,
                "title": album.title,
                "favorite": album.favorite,
                "songs": get_songs_for_album(db, album.id)
            }
            result.append(album_details)

        return result
    
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")
    

def get_songs_for_album(db: Session, album_id: int) -> List[Dict[str, any]]:
    """
    Get the details of songs belonging to a specific album.

    RETURNS:
        - List[dict]: List of dictionaries representing each song's details for the given album.
          Each dictionary has the following keys:
          - "song_id" (int): The unique identifier for the song.
          - "title" (str): The title of the song.
          - "artist" (str): The artist of the song.
          - "release_year" (int): The release year of the song.
          - "favorite" (bool): Indicates whether the song is marked as a favorite.
    """
    try:
        songs = (
            db.query(Music)
            .filter(Music.album_id == album_id)
            .all()
        )

        return [
            {
                "song_id": song.id,
                "album_id": song.album_id,
                "title": song.title,
                "artist": song.artist,
                "release_year": song.release_year,
                
                "favorite": song.favorite
            }
            for song in songs
        ]

    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")