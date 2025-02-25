from fastapi import FastAPI 
from routes.routes import taskRouter
from config.db import create_db 

# Call create_db() to create tables on app startup
create_db()


app = FastAPI()


# Include the task router
app.include_router(taskRouter)
