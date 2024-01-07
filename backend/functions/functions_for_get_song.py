from fastapi import HTTPException
from backend.models import Music
from sqlalchemy.orm import Session


def get_song_by_id(db: Session, song_id: int):
    """
    Fetches the details of a song by its ID from the database.

    PARAMETERS:
        - song_id (int): The ID of the song.

    RETURNS:
        - dict: A dictionary representing the song details. The dictionary has the following keys:
          - "id" (int): The unique identifier of the song.
          - "title" (str): The title of the song.
          - "artist" (str): The artist of the song.
          - "release_year" (int): The release year of the song.
          - "favorite" (bool): Indicates whether the song is marked as a favorite.
    """

    try:
        song = db.query(Music).filter(Music.id == song_id).first()

        if song is None:
            raise HTTPException(status_code=404, detail="Song not found")

        return {
            "id": song.id,
            "title": song.title,
            "artist": song.artist,
            "release_year": song.release_year,
            "favorite": song.favorite,
        }
    
    except Exception as e:
        print(f"An error occurred: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")