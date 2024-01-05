from sqlalchemy.orm import Session
from backend.models import Album

def get_all_albums(db: Session):
    """
    Get a list of all albums in the database.

    Parameters:
    - db (Session): The database session.

    Returns:
    - List[dict]: List of dictionaries representing each album's details.
    """

    albums = db.query(Album).all()
    return [
        {
            "album_id": album.id,
            "title": album.title,
            "favorite": album.favorite,
        }
        for album in albums
    ]