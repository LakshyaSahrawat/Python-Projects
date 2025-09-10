# FastAPI Books CRUD (Modular Structure, Pydantic v2)

## Setup

```bash
python -m venv .venv
source .venv/bin/activate  # or .venv\Scripts\activate on Windows
pip install -r requirements.txt
Run the app
uvicorn app.main:app --reload
Open http://127.0.0.1:8000/docs for Swagger UI.
Tests
pytest -q
Features
•	FastAPI + SQLAlchemy ORM
•	Modular structure (models, schemas, routers, crud, core)
•	Pydantic v2 with Annotated + Field
•	SQLite/Postgres support via .env
•	Custom SQL query (book count)
•	Transaction handling (create_book_with_update)
•	Unit + integration tests ```