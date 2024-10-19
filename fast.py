from fastapi import FastAPI


app = FastAPI()



"""
The @app.get("/") tells FastAPI that the function right below is in charge of handling requests that go to:

    the path /
    using a get operation
"""


# {value in item_id} 
@app.get("/items/{item_id}")
async def read_item(item_id: int):
    return {"item_id is: item_id"}


@app.get("/")
async def root():
    return {"message": "Hello World"}
