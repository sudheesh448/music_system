from database import Base,engine
from models import Music

print("Creating database...")

Base.metadata.create_all(engine)