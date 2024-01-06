from database import Base, engine
from models import Music

print("Creating database...")

try:
    Base.metadata.create_all(engine)
    print("Database created successfully!")
except Exception as e:
    print(f"Error creating database: {e}")