# main.py
import os
from typing import Optional

from fastapi import FastAPI, File, UploadFile, Form, HTTPException, Depends
from sqlalchemy.orm import Session

from backend.database import SessionLocal, engine
# from backend.functions.functions_for_upload import is_mp3_file, save_music_details
from backend.functions.functions_for_listing import get_all_songs
from typing import List
from backend.models import Music, Album


app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/api/music", response_model=List[dict])
async def list_songs(db: Session = Depends(get_db)):
    """
    Get a list of all songs in the database.

    Parameters:
    - db (Session): The database session.

    Returns:
    - List[dict]: List of dictionaries representing each song's details.
    """
    songs = get_all_songs(db)
    return songs

@app.get("/api/albums/{album_id}", response_model=dict)
async def get_album_details(album_id: int, db: Session = Depends(get_db)):


    """
    api call for fetching the album details and associated songs in it
    by using the album id

    PARAMETERS:

    RETURNS:
    --------
    Returns id, title, favorite of albums
    and id, title, artist, release_year,favorite of associated songs

    """

    album = db.query(Album).filter(Album.id == album_id).first()

    if album is None:
        raise HTTPException(status_code=404, detail="Album not found")

    songs = db.query(Music).filter(Music.album_id == album_id).all()

    album_details = {
        "id": album.id,
        "title": album.title,
        "favorite": album.favorite,
        "songs": [{
            "id": song.id,
            "title": song.title,
            "artist": song.artist,
            "release_year": song.release_year,
            "favorite":song.favorite
        } for song in songs]
    }

    return album_details