from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from app import schemas, models, auth
from app.auth import get_current_user, get_db
from app.utils import simulate_task_processing
from app.logging_config import logger

router = APIRouter()

@router.post("/tasks/", response_model=schemas.TaskOut)
def create_task(task: schemas.TaskCreate, background_tasks: BackgroundTasks, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    logger.info(f"User {current_user.username} is creating a task: {task.title}")
    db_task = models.Task(**task.dict(), user_id=current_user.id)
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    logger.info(f"Task created with ID: {db_task.id}")
    background_tasks.add_task(simulate_task_processing, db_task.id, db, models.Task)
    return db_task

@router.get("/tasks/", response_model=list[schemas.TaskOut])
def read_tasks(db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    logger.info(f"User {current_user.username} is fetching their tasks")
    tasks = db.query(models.Task).filter(models.Task.user_id == current_user.id).all()
    logger.info(f"Fetched {len(tasks)} tasks for user {current_user.username}")
    return tasks