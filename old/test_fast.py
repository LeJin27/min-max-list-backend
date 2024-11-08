from enum import Enum
from fastapi import FastAPI
from typing import Optional
from task_database import TaskDatabase
from pydantic import BaseModel




minmax_database = TaskDatabase("localhost", "minmax", "postgres", "dog", 5432)
app = FastAPI()

class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    tax: Optional[float] = None

# One primary argument and 2 optional
# http://127.0.0.1:8000/items/dog?q=string?bool=1
@app.get("/items/{item_id}")
async def read_item(item_id:str, q: Optional[str] = None, short : bool = False):
    item = {"item_id": item_id}
    if q is not None:
        item.update({"q": q})
    if not short:
        item.update(
            {"description": "This is an amazing item that has a long description"}
        )
    return item


@app.post("/items/")
async def create_item(item: Item):
    item_dict = item.dict()
    if item.tax:
        price_with_tax = item.price + item.tax
        item_dict.update({"price_with_tax" : price_with_tax})
    return item




