from fastapi import FastAPI
from contextlib import asynccontextmanager
from database import create_db_and_tables
from dotenv import load_dotenv
from routers.auth import router as auth_router

load_dotenv()

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield

app = FastAPI(lifespan=lifespan)
app.include_router(auth_router)

@app.get("/")
def root():
    return {"hola": "mundo"}