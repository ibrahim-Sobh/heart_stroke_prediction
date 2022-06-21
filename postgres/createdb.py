from database import Base, engine
from models import Patient

print("creating database")

Base.metadata.create_all(engine)

