# models.py
from sqlalchemy import Column, Integer, LargeBinary, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base

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
    music_file_name = Column(String, nullable=False)
    music_file_path = Column(String, nullable=False)
    favorite = Column(Boolean, default=False)
    album = relationship('Album', back_populates='songs')
    
