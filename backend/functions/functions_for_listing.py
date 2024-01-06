from fastapi import HTTPException
from sqlalchemy.orm import Session
from backend.models import Music

def get_all_songs(db: Session):
    """
    Get a list of all songs in the database.

    PARAMETERS

    RETURNS
    - List[dict]: List of dictionaries representing each song's details.
      Each dictionary has the following keys:
      - "song_id" (int): The unique identifier of the song.
      - "album_id" (int or None): The unique identifier of the album to which the song belongs.
      - "title" (str): The title of the song.
      - "artist" (str): The artist of the song.
      - "album" (str or None): The title of the album to which the song belongs.
      - "release_year" (int): The release year of the song.
      - "favorite" (bool): Indicates whether the song is marked as a favorite.
    """

    try:
        songs = db.query(Music).all()
        return [
            {
                "song_id": song.id,
                "album_id": song.album.id if song.album else None,
                "title": song.title,
                "artist": song.artist,
                "album": song.album.title if song.album else None,
                "release_year": song.release_year,
                "favorite": song.favorite
            }
            for song in songs
        ]
    
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")