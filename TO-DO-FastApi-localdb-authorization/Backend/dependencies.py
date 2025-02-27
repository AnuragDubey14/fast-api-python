from fastapi.security import OAuth2PasswordBearer
from config.db import SessionLocal
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
import jwt

# Dependency for getting DB session
def get_db():
    db = SessionLocal()
    try:
        yield db  # Provides a session to the request
    finally:
        db.close()  # Closes the session after the request is complete


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")



