import logging

from dotenv import load_dotenv
from fastapi import FastAPI

from .database import Base, engine
from .routers import auth_router, post_router, user_router

load_dotenv()
logging.basicConfig()
logging.getLogger("sqlalchemy.engine").setLevel(logging.INFO)

Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get("/health_check")
def health_check():
    return {"data": "System is healthy"}

app.include_router(post_router.router)
app.include_router(user_router.router)
app.include_router(auth_router.router)