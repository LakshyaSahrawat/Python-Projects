from fastapi import FastAPI, Request
from database import Base, engine
from routes import users, tasks
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.mount("/static", StaticFiles(directory='static', html=True), name='static')
templates = Jinja2Templates(directory="templates")

app.include_router(users.router, prefix='/user')
app.include_router(tasks.router, prefix='/task')

@app.get("/register", response_class=HTMLResponse)
def register_page(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})

@app.get("/login", response_class=HTMLResponse)
def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.get("/tasks-page", response_class=HTMLResponse)
def tasks_page(request: Request):
    return templates.TemplateResponse("tasks.html", {"request": request})

for route in app.router.routes:
    if hasattr(route, 'methods'):
        print(route.path, route.methods)
