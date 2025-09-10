"""App entrypoint."""
from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.database import init_db
from app.routers import books


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: initialize DB
    await init_db()
    yield
    # Shutdown: add cleanup logic if needed (e.g., closing connections)


app = FastAPI(title="Books CRUD API", lifespan=lifespan)

# Routers
app.include_router(books.router)


@app.get("/")
async def read_root():
    return {"message": "Books CRUD API is up. See /docs for interactive OpenAPI."}