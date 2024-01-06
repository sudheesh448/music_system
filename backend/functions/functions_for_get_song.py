from backend.models import Music
from sqlalchemy.orm import Session


def get_song_by_id(db: Session, song_id: int):
    return db.query(Music).filter(Music.id == song_id).first()