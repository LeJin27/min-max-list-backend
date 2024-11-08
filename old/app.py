from fastapi import FastAPI, HTTPException, Depends, Header
from pydantic import BaseModel
from typing import List, Optional
from task_database import TaskDatabase # Ensure your TaskDatabase class is in this module
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime, timedelta
from fastapi.responses import JSONResponse

USER_DATABASE_NAME = 'minmax'
TASK_SCHEMA = ["task_id", "task_desc", "task_is_completed", "task_created_time_stamp", "user_id"]

# frontend SHOULD not modify task_id and created_time
class Task(BaseModel):
    task_id: int = None  
    task_desc: str
    task_is_completed: bool
    task_created_time_stamp: datetime = None

# convert a list of tuples to base model of task_schema
def helper_tuple_to_task_base_model(list_of_tuples):
    # converts returned tasks to a dictionary
    dict_tasks = [dict(zip(TASK_SCHEMA, task)) for task in list_of_tuples]
    # converts dictionary of tasks to our Pydantic Model 
    pydantic_tasks = [Task(**task_dict) for task_dict in dict_tasks]
    return pydantic_tasks

# Dependency to verify Firebase token
async def get_current_user(id_token: Optional[str] = Header(None)):
    user_id = TaskDatabase.verify_user_token(id_token)
    if user_id is None:
        raise HTTPException(status_code=401, detail="Invalid or missing Firebase token")
    return user_id


# MAIN APP 
#-----------------
app = FastAPI()
user_db = TaskDatabase(host='localhost', dbname=USER_DATABASE_NAME, user='postgres', password='dog', port=5432)
#-----------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # You can specify specific origins instead of "*" for security
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/tasks/", response_model=Task)
async def create_task(task: Task, user_id: str = Depends(get_current_user)):
    user_db.create_user_task(task.task_desc, user_id=user_id)

    all_tasks = user_db.read_user_tasks()
    most_recent_task = helper_tuple_to_task_base_model(all_tasks)[-1]

    # return most recent task infomration to keep track of files 
    return most_recent_task

# tasks/?is_completed=True
# tasks/?is_completed=false
@app.get("/tasks/", response_model=List[Task])
async def read_tasks(task_is_completed: Optional[bool] = None, user_id: str = Depends(get_current_user)):

    if task_is_completed is not None:
        returned_tasks = user_db.read_user_tasks_with_status(task_is_completed)
    else:
        returned_tasks = user_db.read_user_tasks(user_id)

    # convert list of tuples to json
    returned_json = helper_tuple_to_task_base_model(returned_tasks)
    return returned_json

@app.get("/tasks/{task_id}", response_model=List[Task])
async def read_task_id(task_id:int, user_id: str = Depends(get_current_user)):
    returned_json = user_db.read_user_task_id(task_id, user_id)
    return helper_tuple_to_task_base_model(returned_json)

@app.put("/tasks/{task_id}")
async def update_task(task_id: int, task: Task, user_id: str = Depends(get_current_user)):
    user_db.update_user_task(task_id, new_desc=task.task_desc, new_status=task.task_is_completed, user_id=user_id)
    return JSONResponse(content={"message": "Task updated successfully"}, status_code=201)

@app.delete("/tasks/{task_id}")
async def delete_task(task_id: int, user_id: str = Depends(get_current_user)):
    user_db.delete_user_task_by_index(task_id, user_id)
    return JSONResponse(content={"message": "Task deleted successfully"}, status_code=201)



@app.get("/stats/weekly_created")
async def weekly_created_stats(user_id: str = Depends(get_current_user)):
    created_last_week = user_db.get_tasks_created_last_week(user_id)
    return {"tasks_created_last_week": created_last_week}

@app.get("/stats/weekly_completed")
async def weekly_completed_stats(user_id: str = Depends(get_current_user)):
    completed_last_week = user_db.get_tasks_completed_last_week(user_id)
    return {"tasks_completed_last_week": completed_last_week}

@app.get("/stats/weekly_created_completed")
async def weekly_created_completed_stats(start_date: date, user_id: str = Depends(get_current_user)):
    stats = user_db.get_tasks_created_and_completed_week(user_id, start_date)
    return stats

@app.get("/stats/monthly_created")
async def monthly_created_stats(user_id: str = Depends(get_current_user)):
    created_last_month = user_db.get_tasks_created_last_month(user_id)
    return {"tasks_created_last_month": created_last_month}

@app.get("/stats/monthly_completed")
async def monthly_completed_stats(user_id: str = Depends(get_current_user)):
    completed_last_month = user_db.get_tasks_completed_last_month(user_id)
    return {"tasks_completed_last_month": completed_last_month}

@app.get("/stats/monthly_created_completed")
async def monthly_created_completed_stats(month: int, year: int, user_id: str = Depends(get_current_user)):
    stats = user_db.get_tasks_created_and_completed_month(user_id, month, year)
    return stats


