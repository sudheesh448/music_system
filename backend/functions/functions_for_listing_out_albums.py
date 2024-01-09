from fastapi import HTTPException
from sqlalchemy.orm import Session
from backend.models import Album
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
        return [
            {
                "album_id": album.id,
                "title": album.title,
                "favorite": album.favorite,
            }
            for album in albums
        ]
    
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")