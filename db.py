from sqlalchemy import *
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from config.config import config

### Models ### 
from model import Base

db_url = 'mysql+pymysql://{}:{}@{}:{}/{}'.format(
    config["DB_USER"],
    config["DB_PASSWORD"],
    config["DB_HOST"],
    config["DB_PORT"],
    config["DB_DATABASE"],
)

engine = create_engine(
    db_url
)
session_local = sessionmaker(bind=engine)

Base.metadata.create_all(bind=engine)

def get_db():
    db = session_local()
    try:
        yield db
    finally:
        db.close()