# main.py
import os
from typing import Dict, Optional

from fastapi import FastAPI, File, Query, UploadFile, Form, HTTPException, Depends,status,WebSocket
from fastapi.responses import JSONResponse, StreamingResponse
from sqlalchemy.orm import Session
from pathlib import Path
from typing import List
from fastapi.middleware.cors import CORSMiddleware

from backend.database import SessionLocal, engine
from backend.functions.functions_for_get_song import get_song_by_id
from backend.functions.functions_for_listing_out_albums import get_all_albums
from backend.functions.functions_for_upload import is_mp3_file, save_music_details
from backend.functions.functions_for_listing import get_all_songs

from backend.models import Music, Album


app = FastAPI()

origins = [
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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


@app.post("/api/music/upload")
async def upload_file(
    title: str = Form(...),
    artist: str = Form(...),
    album: Optional[str] = Form(None),
    release_year: int = Form(...),
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
)-> JSONResponse:
    
    """
    Handle the file upload and save music details to the database.
    call the is_mp3_file method to check the file is mp3 or not
    if the file is mp3 then the file will be uploaded to the upload folder in the db and call the 
    save save_music_details method for saving the details.

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



@app.get("/api/music/albums")
async def list_albums( db: Session = Depends(get_db),
    page: int = Query(1, description="Page number"),
    size: int = Query(10, description="Number of items per page"),
)-> JSONResponse:
    """
    Get a list of all albums in the database.

    RETURNS:
        List[Dict[str, any]]: List of dictionaries representing each album's details.
        Each dictionary should have the following keys:
           - "album_id": int
           - "title": str
           - "favorite": bool
    """
    try:
        albums = get_all_albums(db, page=page, size=size)
        total_count_album = db.query(Album).count()
        response_data = {
            "success": True,
            "message": "Albums retrieved successfully",
            "page": page,
            "size": size,
            "total_count": total_count_album,
            "data": albums,
            
        }
        
        return JSONResponse(content=response_data, status_code=200)
    except HTTPException as e:
        error_message = str(e.detail)
        response_data = {
            "success": False,
            "message": error_message,
            "page": page,
            "size": size,
            "total_count": total_count_album,
            "data": [],
            
        }
        return JSONResponse(content=response_data, status_code=e.status_code)
    
@app.get("/api/music/songs")
async def list_songs(
    page: int = Query(1, description="Page number"),
    size: int = Query(10, description="Number of items per page"),
    cursor: int = Query(None, description="Cursor for pagination"),
    direction: str = Query("next", description="Pagination direction (next or previous)"),
    db: Session = Depends(get_db)
) -> JSONResponse:
    """
    Get a list of all songs in the database.

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
        songs = get_all_songs(db, page=page, size=size, cursor=cursor, direction=direction)
        total_count_music = db.query(Music).count()
        response_data = {
            "success": True,
            "message": "Songs retrieved successfully",
            "page": page,
            "size": size,
            "total_count": total_count_music,
            "data": songs,
        }
        return JSONResponse(content=response_data, status_code=200)

    except HTTPException as e:
        error_message = str(e.detail)
        response_data = {
            "success": False,
            "message": error_message,
            "page": page,
            "size": size,
            "total_count": 0,  # Set total_count to 0 in case of an error
            "data": [],
        }
        return JSONResponse(content=response_data, status_code=e.status_code)

    except HTTPException as e:
        error_message = str(e.detail)
        response_data = {
            "success": False,
            "message": error_message,
            "page": page,
            "size": size,
            "total_count": total_count_music,
            "data": [],
        }
        return JSONResponse(content=response_data, status_code=e.status_code)

@app.get("/api/music/albums/{album_id}")
async def get_album_details(album_id: int, db: Session = Depends(get_db))-> JSONResponse:
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
            "success": True,
            "message": f"Details of album with ID {album_id} retrieved successfully.",
            "data": {
                "id": album.id,
                "title": album.title,
                "favorite": album.favorite,
                "songs": [{
                    "id": song.id,
                    "title": song.title,
                    "artist": song.artist,
                    "release_year": song.release_year,
                    "favorite": song.favorite
                } for song in songs]
            }
        }
        return JSONResponse(content=album_details, status_code=200)

    except HTTPException as e:
        response_data = {
            "success": False,
            "message": str(e.detail),
            "data": []
        }
        raise HTTPException(status_code=e.status_code, detail=response_data)
    
    except:
        response_data = {
            "success": False,
            "message": "Internal Server Error",
            "data": []
        }
        raise HTTPException(status_code=500, detail=response_data)


@app.get("/api/music/song/{song_id}")
async def get_song_details(song_id: int, db: Session = Depends(get_db))-> JSONResponse:
    """
    Get details of a specific song by its ID.

    RETURNS:
        - dict: Dictionary representing the song's details.
          The dictionary has the following keys:
          - "id" (int): The unique identifier of the song.
          - "title" (str): The title of the song.
          - "artist" (str): The artist of the song.
          - "release_year" (int): The release year of the song.
          - "favorite" (bool): Indicates whether the song is marked as a favorite.
          - "album id" (int) : Indicates the ID of the particular album.
          - "album name" (str): Indicates the name of the album
    """
    try:
        song = db.query(Music).filter(Music.id == song_id).first()

        if song is None:
            raise HTTPException(status_code=404, detail="Song not found")
        
        album_id = song.album_id
        album_title = None
        if album_id:
            album = db.query(Album).filter(Album.id == album_id).first()
            if album:
                album_title = album.title

        song_details = {
            "success": True,
            "message": f"Details of song with ID {song_id} retrieved successfully.",
            "data": {
                "id": song.id,
                "title": song.title,
                "artist": song.artist,
                "release_year": song.release_year,
                "favorite": song.favorite,
                "album_id": album_id,
                "album_title": album_title,
            }
        }

        return JSONResponse(content=song_details, status_code=200)
    
    except HTTPException as e:
        response_data = {
            "success": False,
            "message": str(e.detail),
            "data": []
        }
        raise HTTPException(status_code=e.status_code, detail=response_data)
    
    except:
        response_data = {
            "success": False,
            "message": "Internal Server Error",
            "data": []
        }
        raise HTTPException(status_code=500, detail=response_data)
    


websocket_connections = {}

@app.websocket("/music/song/{song_id}/stream")
async def stream_music_file(
    websocket: WebSocket,
    song_id: int,
    db: Session = Depends(get_db)
):
    """
    Stream the music file associated with a given song ID with pause, seek, and fwd/rvs functionality.

    PARAMETERS:
        - websocket: WebSocket connection
        - song_id: The unique identifier of the song.

    Returns:
        - WebSocket communication for streaming the music file.
    """
    print("here")
    try:
        file_path = db.query(Music.music_file_path).filter(Music.id == song_id).scalar()

        if file_path is None:
            raise HTTPException(status_code=404, detail="Song not found")
        
        if not Path(file_path).is_file():
            raise HTTPException(status_code=404, detail=f"File not found: {file_path}")

        # Send the initial chunk of the file
        await websocket.accept()
        await websocket.send_bytes(open(file_path, "rb").read(1024))

        # Store the WebSocket connection
        websocket_connections[song_id] = websocket

        while True:
            # Receive commands from the client
            data = await websocket.receive_text()

            if data == "pause":
                # Pause streaming
                continue
            elif data.startswith("seek:"):
                # Seek to a specific position (in seconds)
                position = int(data.split(":")[1])
                # Implement logic to seek to the specified position
                continue
            elif data == "fwd":
                # Forward (skip ahead)
                # Implement logic to skip forward
                continue
            elif data == "rvs":
                # Reverse (skip backward)
                # Implement logic to skip backward
                continue
            elif data == "close":
                # Close the WebSocket connection
                await websocket.close()
                break

    except HTTPException as e:
        if e.status_code == 404:
            await websocket.send_text(f"Error: {e.detail}")
        raise

    except Exception as ex:
        await websocket.send_text("Internal Server Error")

    finally:
        # Remove the WebSocket connection when the client disconnects
        del websocket_connections[song_id]

# Example of notifying the WebSocket for updates (you can call this from another part of your code)
async def notify_song_update(song_id: int, data: bytes):
    if song_id in websocket_connections:
        await websocket_connections[song_id].send_bytes(data)

        

@app.patch("/api/music/song/{song_id}/favorite")
async def favorite_music(song_id: int, db: Session = Depends(get_db))-> JSONResponse:
    """
    Mark a song as a favorite.

    RETURNS:
        - JSONResponse: A JSON response containing a success message and the song details.
    """
    try:
        song = db.query(Music).filter(Music.id == song_id).first()

        if not song:
            raise HTTPException(status_code=404, detail="Song not found")

        song.favorite = not song.favorite
        db.commit()

        updated_song_details = {
            "success": True,
            "message": f"Song with ID {song_id} has been marked as {'favorite' if song.favorite else 'not favorite'}.",
            "data": {
                "id": song.id,
                "title": song.title,
                "artist": song.artist,
                "release_year": song.release_year,
                "favorite": song.favorite,
            }
        }

        return JSONResponse(content=updated_song_details, status_code=200)

    except HTTPException as e:
        if e.status_code == 404:
            response_data = {
                "success": False,
                "message": str(e.detail),
                "data": []
            }
            raise HTTPException(status_code=404, detail=response_data)
        raise
    except:
        response_data = {
            "success": False,
            "message": "Internal Server Error",
            "data": []
        }
        raise HTTPException(status_code=500, detail=response_data)
    

@app.delete("/api/music/song/{song_id}")
async def delete_song(song_id: int, db: Session = Depends(get_db)) -> JSONResponse:
    """
    Delete a song by its ID.

    RETURNS:
        - JSONResponse: A JSON response indicating the success of the deletion.
    """
    try:
        song = db.query(Music).filter(Music.id == song_id).first()

        if song is None:
            raise HTTPException(status_code=404, detail="Song not found")

        file_path = song.music_file_path
        if file_path:
            
            directory = Path(file_path).parent
            directory.mkdir(parents=True, exist_ok=True)

          
            if os.path.exists(file_path):
                os.remove(file_path)

        db.delete(song)
        db.commit()

        response_data = {
            "success": True,
            "message": f"Song with ID {song_id} has been deleted successfully.",
        }

        return JSONResponse(content=response_data, status_code=200)

    except HTTPException as e:
        if e.status_code == 404:
            response_data = {
                "success": False,
                "message": str(e.detail),
            }
            raise HTTPException(status_code=404, detail=response_data)
        raise
    except:
        response_data = {
            "success": False,
            "message": "Internal Server Error",
        }
        raise HTTPException(status_code=500, detail=response_data)

@app.delete("/api/music/album/{album_id}")
async def delete_album(album_id: int, db: Session = Depends(get_db)) -> JSONResponse:
    """
    Delete an album by its ID.

    RETURNS:
        - JSONResponse: A JSON response indicating the success of the deletion.
    """
    try:
        album = db.query(Album).filter(Album.id == album_id).first()

        if album is None:
            raise HTTPException(status_code=404, detail="Album not found")

        for song in album.songs:
            file_path = song.music_file_path
            if file_path:
                directory = Path(file_path).parent
                directory.mkdir(parents=True, exist_ok=True)
                if os.path.exists(file_path):
                    os.remove(file_path)

            db.delete(song)
        db.delete(album)
        db.commit()

        response_data = {
            "success": True,
            "message": f"Album with ID {album_id} has been deleted successfully.",
        }

        return JSONResponse(content=response_data, status_code=200)

    except HTTPException as e:
        if e.status_code == 404:
            response_data = {
                "success": False,
                "message": str(e.detail),
            }
            raise HTTPException(status_code=404, detail=response_data)
        raise
    except:
        response_data = {
            "success": False,
            "message": "Internal Server Error",
        }
        raise HTTPException(status_code=500, detail=response_data)
