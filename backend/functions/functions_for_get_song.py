from backend.models import Music
from sqlalchemy.orm import Session


def get_song_by_id(db: Session, song_id: int):
    
    """
    Function for fetching the song details by using song id from db.

    PARAMETER:
    song_id

    RETURNS:
    Returning the song details

    """

    return db.query(Music).filter(Music.id == song_id).first()