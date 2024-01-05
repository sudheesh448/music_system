# main.py
import os
from typing import Optional

from fastapi import FastAPI, File, UploadFile, Form, HTTPException, Depends
from sqlalchemy.orm import Session

from backend.database import SessionLocal, engine
from backend.functions.functions_for_upload import is_mp3_file, save_music_details
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