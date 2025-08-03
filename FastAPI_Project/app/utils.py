import time

def simulate_task_processing(task_id: int, db_session, Task):
    time.sleep(5)
    db_task = db_session.query(Task).get(task_id)
    if db_task:
        db_task.status = "completed"
        db_session.commit()