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


@app.post("/api/upload")
async def upload_file(
    title: str = Form(...),
    artist: str = Form(...),
    album: Optional[str] = Form(None),
    release_year: int = Form(...),
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    
    """
    Handle the file upload and save music details to the database.\
    call the is_mp3_file method to check the file is mp3 or not
    if the file is mp3 then the file will be uploaded to the upload folder in the db and call the 
    save save_music_details method for saving the details.

    Parameters:
    - title (str): The title of the music.
    - artist (str): The artist of the music.
    - album (Optional[str]): The title of the album (can be None if no album is specified).
    - release_year (int): The release year of the music.
    - file (UploadFile): The uploaded MP3 file.
    - db (Session): The database session.

    Returns:
    - dict: A message indicating the success of the file upload and details save.
    """

    try:
        if not is_mp3_file(file.filename):
            raise HTTPException(status_code=400, detail="Invalid file format. Only MP3 files are allowed.")

        upload_folder = 'uploads'
        os.makedirs(upload_folder, exist_ok=True)
        file_path = os.path.join(upload_folder, file.filename)
        with open(file_path, "wb") as f:
            f.write(file.file.read())

        save_music_details(db, title, artist, album, release_year, file.filename)

        return {"message": "File successfully uploaded and details saved"}
    except Exception as e:
        print("error", e)
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
