from sqlalchemy import create_engine,MetaData
from sqlalchemy.orm import sessionmaker, scoped_session, declarative_base

DATABASE_URL = "sqlite:///./tasks.db" 

# Create the database engine
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

# Create a SessionLocal class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for ORM models
Base = declarative_base()
meta=MetaData()

# Dependency for getting DB session
def get_db():
    db = SessionLocal()
    try:
        yield db  # Provides a session to the request
    finally:
        db.close()  # Closes the session after the request is complete


# Function to create tables explicitly if they don't exist
def create_db():
    print("Creating tables if they do not exist...")
    # Ensure the tables are created
    Base.metadata.create_all(bind=engine)
    print("Tables created successfully.")

