from sqlalchemy.orm import Session
from backend.models import Music

def get_all_songs(db: Session):
    """
    Get a list of all songs in the database.

    :PARAMETERS
    -----------
    db: Object of the Session ORM. 

    :RETURNS
    --------
    - List[dict]: List of dictionaries representing each song's details.
    """

    songs = db.query(Music).all()
    return [
        {
            "song_id": song.id,
            "album_id": song.album.id if song.album else None,
            "title": song.title,
            "artist": song.artist,
            "album": song.album.title if song.album else None,
            "release_year": song.release_year,
            "favorite":song.favorite
        }
        for song in songs
    ]