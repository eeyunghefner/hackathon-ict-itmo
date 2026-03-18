from fastapi import FastAPI
from .routers import router

from contextlib import asynccontextmanager
import dotenv
from pathlib import Path
import os

dotenv.load_dotenv()

app = FastAPI(title="API Hackathon Server", version="1.0.0")

app.include_router(router)
