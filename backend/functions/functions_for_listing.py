from fastapi import HTTPException
from sqlalchemy import desc
from sqlalchemy.orm import Session

from backend.models import Music


def get_all_songs(db: Session, page: int = 1, size: int = 10, cursor: int = None, direction: str = "next"):
    try:
        query = db.query(Music)

        if direction == "next":
            if cursor is not None:
                query = query.filter(Music.id > cursor).order_by(Music.id)
        elif direction == "previous":
            if cursor is not None:
                query = query.filter(Music.id < cursor).order_by(desc(Music.id))

        query = query.limit(size) 

        songs = query.all()

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
