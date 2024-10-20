from fastapi import FastAPI
from database import TaskDatabase
from typing import Optional

minmax_database = TaskDatabase("localhost", "minmax", "postgres", "dog", 5432)
print(minmax_database.read_all_is_open_task(True))

app = FastAPI()



"""
The @app.get("/") tells FastAPI that the function right below is in charge of handling requests that go to:

    the path /
    using a get operation
"""


# {value in item_id} 
"""
Resource usage
http://127.0.0.1:8000/tasks/?index=4           //Returns task at index 4
http://127.0.0.1:8000/tasks/?is_open=True      //Returns all tasks that are open
http://127.0.0.1:8000/tasks/?is_open=False     //Returns all taks that are closed
"""
@app.get("/tasks")
async def read_tasks(index: Optional[int] = None, is_open: Optional[bool] = None):
    if is_open is not None:
        if (is_open):
            return minmax_database.read_all_is_open_task(True)
        else: 
            return minmax_database.read_all_is_open_task(False)

    if index is not None: 
        return minmax_database.read_at_task(index)

    return minmax_database.read_all_tasks()





