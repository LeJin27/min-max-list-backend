from fastapi import FastAPI
from database import TaskDatabase
from typing import Optional

minmax_database = TaskDatabase("localhost", "minmax", "postgres", "dog", 5432)
print(minmax_database.read_all_is_open_task(True))

app = FastAPI()

# ? are query parameters
# {} are resources 


# {value in item_id} 
"""
Resource usage
http://127.0.0.1:8000/tasks/{index}             //returns task at index
"""
@app.get("/tasks/{index}")
async def read_tasks_id(index:int):
    return minmax_database.read_at_task(index)


"""
http://127.0.0.1:8000/tasks/?is_open=True      //Returns all tasks that are open
http://127.0.0.1:8000/tasks/?is_open=False     //Returns all taks that are closed
"""

@app.get("/tasks")
async def read_tasks(is_open: Optional[bool] = None):
    if is_open is not None:
        if (is_open):
            return minmax_database.read_all_is_open_task(True)
        else: 
            return minmax_database.read_all_is_open_task(False)

    return minmax_database.read_all_tasks()





