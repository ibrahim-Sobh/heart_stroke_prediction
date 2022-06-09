from sqlalchemy.orm import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import config 


connection_url = config.get_Settings()

print(connection_url)

engine = create_engine(connection_url, echo=True)

Base = declarative_base()

SessionLocal = sessionmaker(bind=engine)
