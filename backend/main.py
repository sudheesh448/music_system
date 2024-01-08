# main.py
import os
from typing import Optional

from fastapi import FastAPI, File, UploadFile, Form, HTTPException, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from backend.database import SessionLocal, engine
from backend.functions.functions_for_get_song import get_song_by_id
from backend.functions.functions_for_listing_out_albums import get_all_albums
from backend.functions.functions_for_upload import is_mp3_file, save_music_details
from backend.functions.functions_for_listing import get_all_songs
from typing import List
from backend.models import Music, Album


app = FastAPI()

def get_db():
    """
    Provides a database session for interacting with the database.

    Yields:
        Session: An instance of the database session. 
    """
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
    Handle the file upload and save music details to the database.
    call the is_mp3_file method to check the file is mp3 or not
    if the file is mp3 then the file will be uploaded to the upload folder in the db and call the 
    save save_music_details method for saving the details.

    PARAMETERS:

    RETRUNS:
        - A Json response and status code indicating the success or failure 
        of the file upload and details save.
    """
    try:
        if not is_mp3_file(file.filename):
                raise HTTPException(status_code=400, detail="Invalid file format. Only MP3 files are allowed.")
            
        mp3_data = file.file.read()
            
        save_music_details(db=db, title=title, artist=artist, album_title=album, release_year=release_year, mp3_data=mp3_data)
        print("here root")
        response_data = {"message": "File successfully uploaded and details saved"}
        return JSONResponse(content=response_data, status_code=200)
    
    except Exception as unexpected_error:
        return JSONResponse(content={"error": "Internal Server Error"}, status_code=500)



@app.get("/api/albums", response_model=List[dict])
async def list_albums(db: Session = Depends(get_db)):
    """
    Get a list of all albums in the database.

    PARAMETERS:


    RETURNS:
        List[Dict[str, any]]: List of dictionaries representing each album's details.
        Each dictionary should have the following keys:
           - "album_id": int
           - "title": str
           - "favorite": bool
    """
    try:
        albums = get_all_albums(db)
        return JSONResponse(content=albums, status_code=200)
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")

    
@app.get("/api/music", response_model=List[dict])
async def list_songs(db: Session = Depends(get_db)):
    """
    Get a list of all songs in the database.

    PARAMETERS:
    

    RETURNS:
        - List[dict]: List of dictionaries representing each song's details.
          Each dictionary should have the following keys:
          - "song_id": int - The unique identifier for the song.
          - "album_id": int or None - The unique identifier for the album to which the song belongs.
          - "title": str - The title of the song.
          - "artist": str - The artist of the song.
          - "album": str or None - The title of the album to which the song belongs.
          - "release_year": int - The release year of the song.
          - "favorite": bool - Indicates whether the song is marked as a favorite.
    """
    
    try:
        songs = get_all_songs(db)
        return JSONResponse(content=songs, status_code=200)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")

@app.get("/api/albums/{album_id}", response_model=dict)
async def get_album_details(album_id: int, db: Session = Depends(get_db)):
    """"
    API endpoint for fetching the details of an album and its associated songs.

    PARAMETERS:
        - album_id (int): The unique identifier of the album.

    RETURNS:
        - Dict: A dictionary representing the album details and associated songs.
          The dictionary has the following keys:
          - "id" (int): The unique identifier of the album.
          - "title" (str): The title of the album.
          - "favorite" (bool): Indicates whether the album is marked as a favorite.
          - "songs" (List[Dict]): A list of dictionaries representing each associated song's details.

            Each song dictionary has the following keys:
            - "id" (int): The unique identifier of the song.
            - "title" (str): The title of the song.
            - "artist" (str): The artist of the song.
            - "release_year" (int): The release year of the song.
            - "favorite" (bool): Indicates whether the song is marked as a favorite.
    """
    try:
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
        return JSONResponse(content=album_details, status_code=200)
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")


@app.get("/api/music/song/{song_id}", response_model=dict)
async def get_song_details(song_id: int, db: Session = Depends(get_db)):
    """
    Get details of a specific song by its ID.

    PARAMETERS:
        - song_id (int): The ID of the song.

    RETURNS:
        - dict: Dictionary representing the song's details.
          The dictionary has the following keys:
          - "id" (int): The unique identifier of the song.
          - "title" (str): The title of the song.
          - "artist" (str): The artist of the song.
          - "release_year" (int): The release year of the song.
          - "favorite" (bool): Indicates whether the song is marked as a favorite.
    """
    try:
        song = get_song_by_id(db, song_id)

        if song is None:
            raise HTTPException(status_code=404, detail="Song not found")

        song_details = {
            "id": song.id,
            "title": song.title,
            "artist": song.artist,
            "release_year": song.release_year,
            "favorite": song.favorite,
        }
        return JSONResponse(content=song_details, status_code=200)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")