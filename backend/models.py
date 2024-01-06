# models.py
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey,LargeBinary
from sqlalchemy.orm import relationship
from .  database import Base

class Album(Base):
    __tablename__ = 'albums'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True, nullable=True)
    favorite = Column(Boolean, default=False)
    songs = relationship('Music', back_populates='album', cascade='all, delete-orphan')

class Music(Base):
    __tablename__ = 'music'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True, nullable=False)
    artist = Column(String, index=True, nullable=False)
    album_id = Column(Integer, ForeignKey('albums.id', ondelete='CASCADE'), nullable=True)
    release_year = Column(Integer)
    mp3_data = Column(LargeBinary, nullable=False)  # New column for storing MP3 data
    favorite = Column(Boolean, default=False)
    album = relationship('Album', back_populates='songs')
