from sqlalchemy import create_engine,MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

load_dotenv()
DB_URL = DB_URL = os.getenv("DB_URL")
engine = create_engine(DB_URL,echo=True)
SessionLocal = sessionmaker(autocommit=False,autoflush=False, bind=engine)

Base = declarative_base()
meta=MetaData()


# Function to create tables explicitly if they don't exist
def create_db():
    print("Creating tables if they do not exist...")
    # Ensure the tables are created
    Base.metadata.create_all(bind=engine)
    print("Tables created successfully.")

