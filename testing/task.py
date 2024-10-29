from fastapi import FastAPI, Depends, HTTPException, status
from firebase_admin import auth, credentials, initialize_app
from typing import List
from pydantic import BaseModel
import psycopg2

# Initialize Firebase Admin SDK
cred = credentials.Certificate("/Users/pujitha/Downloads/to-do-list.json")
initialize_app(cred)

# Initialize FastAPI app
app = FastAPI()

# Database Constants
TASK_PRIMARY_KEY = "task_id"
TASK_DESCRIPTION = "task_desc"
TASK_IS_COMPLETED = "task_is_completed"
TASK_CREATED_TIME_STAMP = "task_created_time_stamp"
USER_ID = "user_id"

# Database Connection
class TaskDatabase:
    def __init__(self, host, dbname, user, password, port):
        self.connection = psycopg2.connect(
            host=host, dbname=dbname, user=user, password=password, port=port
        )
        self.cursor = self.connection.cursor()
        self.create_table()

    def create_table(self):
        self.cursor.execute(f"""
            CREATE TABLE IF NOT EXISTS tasks (
                {TASK_PRIMARY_KEY} SERIAL PRIMARY KEY, 
                {TASK_DESCRIPTION} VARCHAR(255), 
                {TASK_IS_COMPLETED} BOOLEAN,
                {TASK_CREATED_TIME_STAMP} TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
                {USER_ID} VARCHAR(255)
            );
        """)
        self.connection.commit()

    def create_task(self, task_desc, user_id):
        self.cursor.execute(f"""
            INSERT INTO tasks ({TASK_DESCRIPTION}, {TASK_IS_COMPLETED}, {USER_ID})
            VALUES (%s, %s, %s);
        """, (task_desc, False, user_id))
        self.connection.commit()

    def read_user_tasks(self, user_id):
        self.cursor.execute(f"SELECT * FROM tasks WHERE {USER_ID} = %s;", (user_id,))
        return self.cursor.fetchall()

    ...

# Initialize TaskDatabase instance
db = TaskDatabase("localhost", "to_do_list", "postgres", "dog", 5433)

# Pydantic model for task creation
class Task(BaseModel):
    description: str

# Firebase token verification
def verify_firebase_token(id_token: str):
    try:
        decoded_token = auth.verify_id_token(id_token)
        user_id = decoded_token["uid"]
        return user_id
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
        )

# Dependency for verifying Firebase tokens
async def get_current_user(id_token: str):
    user_id = verify_firebase_token(id_token)
    return user_id

### 3. FastAPI Endpoints

# Task creation endpoint
@app.post("/tasks", status_code=201)
async def create_task(task: Task, user_id: str = Depends(get_current_user)):
    db.create_task(task.description, user_id)
    return {"message": "Task created successfully"}

# Endpoint to get all tasks for a user
@app.get("/tasks", response_model=List[dict])
async def get_user_tasks(user_id: str = Depends(get_current_user)):
    tasks = db.read_user_tasks(user_id)
    return [{"task_id": t[0], "description": t[1], "is_completed": t[2]} for t in tasks]




# Run FastAPI server with: uvicorn main:app --reload
