from fastapi import FastAPI 
from routes.routes import taskRouter

# Import the function to create tables
from config.db import create_db # This should match the function name in db.py

# Call create_db() to create tables on app startup
create_db()


app = FastAPI()


# Include the task router
app.include_router(taskRouter)
