from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from task_database import TaskDatabase  # Ensure your TaskDatabase class is in this module
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional
from datetime import datetime
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

USER_DATABASE_NAME = 'minmax'
TASK_SCHEMA = ["task_id", "task_desc", "task_is_completed", "task_created_time_stamp"]

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
async def create_task(task: Task ):
    user_db.create_task(task.task_desc)

    all_tasks = user_db.read_all_tasks()
    most_recent_task = helper_tuple_to_task_base_model(all_tasks)[-1]

    # return most recent task infomration to keep track of files 
    return most_recent_task

# tasks/?is_completed=True
# tasks/?is_completed=false
@app.get("/tasks/", response_model=List[Task])
async def read_tasks(task_is_completed: Optional[bool] = None):

    if task_is_completed is not None:
        if (task_is_completed):
            returned_tasks = user_db.read_tasks_with_status(True)
        else: 
            returned_tasks = user_db.read_tasks_with_status(False)
    else:
        returned_tasks = user_db.read_all_tasks()

    # convert list of tuples to json
    returned_json = helper_tuple_to_task_base_model(returned_tasks)
    return returned_json

@app.get("/tasks/{task_id}", response_model=List[Task])
async def read_task_id(task_id:int):
    returned_json = user_db.read_at_task_id(task_id)
    return helper_tuple_to_task_base_model(returned_json)


@app.put("/tasks/{task_id}")
async def update_task(task_id: int, task: Task):
    user_db.update_task(task_id, new_desc=task.task_desc, new_status=task.task_is_completed)
    return JSONResponse(content={"message": "Task updated successfully"}, status_code=201)

@app.delete("/tasks/{task_id}")
async def delete_task(task_id: int):
    user_db.delete_task_by_index(task_id)
    return JSONResponse(content={"message": "Task deleted successfully"}, status_code=201)