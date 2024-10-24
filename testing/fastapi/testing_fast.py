from fastapi import FastAPI
from database import TaskDatabase
from typing import Optional
from pydantic import BaseModel

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
    return minmax_database.read_at_task_id(index)


"""
http://127.0.0.1:8000/tasks/?is_open=True      //Returns all tasks that are open
http://127.0.0.1:8000/tasks/?is_open=False     //Returns all taks that are closed
"""

@app.get("/tasks")
async def read_tasks(task_is_completed: Optional[bool] = None):
    if task_is_completed is not None:
        if (task_is_completed):
            return minmax_database.read_all_is_open_task(True)
        else: 
            return minmax_database.read_all_is_open_task(False)

    return minmax_database.read_all_tasks()

class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    tax: Optional[float] = None

@app.post("/items/")
async def create_item(item: Item):
    item_dict = item.dict()
    if item.tax:
        price_with_tax = item.price + item.tax
        item_dict.update({"price_with_tax": price_with_tax})
    return item_dict



