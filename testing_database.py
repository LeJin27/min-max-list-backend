from database import TaskDatabase



Test = TaskDatabase
USER_DATABASE_NAME = 'minmax'
user_db = TaskDatabase(host='localhost', dbname=USER_DATABASE_NAME, user='postgres', password='dog', port=5432)

user_db.create_task("Teoadsjkdfh")
user_db.create_task("CAt")

for task in user_db.read_all_tasks():
    print(task)
