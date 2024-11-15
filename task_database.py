import psycopg2
from datetime import datetime
import pytz

"""
Used to create a data for all todo related functions 

create_database 
create_table 
---
Different queries
---
update_task
create_task  
delete_task 
read_task_done
read_task_not_done
"""

TASK_PRIMARY_KEY = "task_id"
TASK_UID = "task_uid"
TASK_LIST = "task_list"
TASK_DESCRIPTION = "task_desc"
TASK_IS_COMPLETED = "task_is_completed"
TASK_CREATED_TIME_STAMP = "task_created_time_stamp"
TASK_UPDATED_TIME_STAMP = "task_updated_time_stamp"
TASK_ALARM_TIME = "task_alarm_time"
TASK_DUE_DATE = "task_due_date"




class TaskDatabase:
    # Use localhost, minmax, postgres, your password, 5432 
    def __init__(self, host, dbname, user, password, port):
        """
        basic connector for database. Should setup table and database if none can be found.
        """

        self.dbname = dbname
        self.user = user
        self.password = password
        self.host = host
        self.port = port

        # Try to connect to database. If unable to, create new database.
        try:
            self.connection = psycopg2.connect(host=self.host, dbname = self.dbname, user=self.user, password=self.password, port = self.port)
            self.cursor = self.connection.cursor()
            print(f"Database '{self.dbname}' found and connected.")
        except Exception as e:
            if "does not exist" in str(e):
                # update cursor after new connection
                self.create_database()
                self.connection.close()
                self.connection = psycopg2.connect(host=self.host, dbname = self.dbname, user=self.user, password=self.password, port = self.port)
                self.cursor = self.connection.cursor()
            else: 
                print("Something really went wrong")
        

        self.create_table()
        

    
    def create_table(self):
        # Creating Table of Tasks
        print("Creating tasks table")
        self.connection.autocommit = True  
        try:
            self.cursor.execute(f"""
                    CREATE TABLE IF NOT EXISTS tasks (
                    {TASK_PRIMARY_KEY} SERIAL PRIMARY KEY, 
                    {TASK_UID} VARCHAR(255),
                    {TASK_LIST} VARCHAR(255),
                    {TASK_DESCRIPTION} VARCHAR(255), 
                    {TASK_IS_COMPLETED} BOOLEAN,
                    {TASK_CREATED_TIME_STAMP} TIMESTAMPTZ,
                    {TASK_ALARM_TIME} TIMESTAMPTZ,
                    {TASK_DUE_DATE} TIMESTAMPTZ
                    );
                    """)
        except Exception as e:
            print("Something when wrong")
    

    def create_database(self):
        """
        Initialize database. Used in initializer if a database cannot be found
        """

        # Connect default postgres database to create the new database
        self.connection = psycopg2.connect(dbname="postgres", user=self.user, password=self.password, host=self.host)
        self.connection.autocommit = True  
        self.cursor = self.connection.cursor()

        try:
            self.cursor.execute('CREATE DATABASE ' + self.dbname)
            print(f"Database '{self.dbname}' created successfully.")

        except Exception as e:
            print(f"Error creating database: {e}")
    

    
    def create_task(self, task_uid, task_list, task_desc, task_alarm_time=None, task_due_date=None):
        """
        Creates basic task which is automatically set to false completed. Needs time implementation.
        """
        # print(f"Task Alarm Time: {task_alarm_time}, Type: {type(task_alarm_time)}")

        try:
            # check if alarm is string or datetime and handle appropiately
            if task_alarm_time:
                if isinstance(task_alarm_time, str):
                    task_alarm_time = datetime.fromisoformat(task_alarm_time)

                if isinstance(task_alarm_time,datetime):
                    task_alarm_time = task_alarm_time.astimezone(pytz.UTC)

            if task_due_date:
                if isinstance(task_due_date, str):
                    task_due_date = datetime.fromisoformat(task_due_date)

                if isinstance(task_due_date,datetime):
                    task_due_date = task_due_date.astimezone(pytz.UTC)

            self.cursor.execute(f"""
                INSERT INTO tasks({TASK_UID}, {TASK_LIST}, {TASK_DESCRIPTION}, {TASK_IS_COMPLETED}, {TASK_CREATED_TIME_STAMP},{TASK_ALARM_TIME},{TASK_DUE_DATE})
                VALUES (%s, %s, %s, %s, CURRENT_TIMESTAMP, %s, %s);
            """, (task_uid,task_list, task_desc, False, task_alarm_time, task_due_date))
        except Exception as e:
            print(f"Error creating task: {e}")
        
        self.connection.commit()
    
    def get_unique_task_lists(self, uid):
        try:
            self.cursor.execute(f"""
                SELECT DISTINCT {TASK_LIST} 
                FROM tasks 
                WHERE {TASK_UID} = %s;
            """, (uid,))

            unique_task_lists = [row[0] for row in self.cursor.fetchall()]
            return unique_task_lists

        except Exception as e:
            print("Something went wrong:", e)
            return []


    def read_all_tasks(self, task_uid, task_list=None, task_is_completed = None,task_created_time_stamp=None, task_due_date = None):
        """
        Reads all tasks, filtered by uid and optionally by task_list.
        """
        try:
            # Build the base query
            query = f"SELECT * FROM tasks WHERE {TASK_UID} = %s"
            params = [task_uid]

            # Add optional task_list filter
            if task_list is not None:
                query += f" AND {TASK_LIST} = %s"
                params.append(task_list)

            if task_is_completed is not None:
                query += f" AND {TASK_IS_COMPLETED} = %s"
                params.append(task_is_completed)

            # add optional timestamp filter using DATE() to ignore time
            if task_created_time_stamp is not None:
                query += f" AND DATE({TASK_CREATED_TIME_STAMP}) = %s"
                params.append(task_created_time_stamp)

            if task_due_date is not None:
                query += f" AND DATE({TASK_DUE_DATE}) = %s"
                params.append(task_due_date)

            # use custom built query and input user variables
            self.cursor.execute(query, tuple(params))

            tasks = self.cursor.fetchall()
            return tasks

        except Exception as e:
            print(f"Error reading tasks: {e}")
            return None
    


    
    def read_at_task_id(self, index):
        """
        Reads task at index i
        """
        try:
            self.cursor.execute(f"""
                    SELECT * FROM tasks WHERE {TASK_PRIMARY_KEY} = {index}
                    """);
        except Exception as e:
            print(f"Error reading task: {e}")
        
        self.connection.commit()

        all_tasks = self.cursor.fetchall()
        return all_tasks


    def read_tasks_with_status(self, task_uid, status, task_list=None):
        """
        Reads all tasks with a specified completion status (True or False), optionally filtered by task_uid and task_list.
        """
        try:
            if task_list is not None:
                # Filter by task_uid, status, and task_list
                self.cursor.execute(f"""
                    SELECT * FROM tasks 
                    WHERE {TASK_IS_COMPLETED} = %s AND {TASK_UID} = %s AND {TASK_LIST} = %s
                    """, (status, task_uid, task_list))
            else:
                # Filter only by task_uid and status
                self.cursor.execute(f"""
                    SELECT * FROM tasks 
                    WHERE {TASK_IS_COMPLETED} = %s AND {TASK_UID} = %s
                    """, (status, task_uid))

            # Fetch all matching tasks
            all_tasks = self.cursor.fetchall()
            return all_tasks

        except Exception as e:
            print(f"Error reading tasks: {e}")
            return None



    def delete_all_tasks(self):
        """
        Deletes all tasks from the database
        """
        try:
            self.cursor.execute("""
            DELETE FROM tasks
            """)
            print("Deleted all tasks")
        except Exception as e:
            print(f"Error deleting all tasks: {e}")

    def delete_task_by_index(self,index):
        """
        Deletes a task from the database using the index
        """
        try:
            # fetches task  useing %s to only catch string type arguments 
            self.cursor.execute(f"""
                SELECT * FROM tasks WHERE {TASK_PRIMARY_KEY} = %s
                """, (index,))
            task = self.cursor.fetchone()

            #if task found delete otherwise print not found
            if task:
                print(f"Deleting task: {task}")

                self.cursor.execute(f"""
                    DELETE FROM tasks WHERE {TASK_PRIMARY_KEY} = %s 
                    """,(index,))
            else:
                print(f"No task found with index: {index}")
        except Exception as e:
            print(f"Error deleting task by index: {e}")
        self.connection.commit()

    def delete_task_by_desc(self,desc):
        """
        Deletes a task from the database using the task_desc.
        Note! deletes all instances of task_desc if there are multiple with the same task_desc
        """
        try:
            self.cursor.execute(f"""
                    DELETE FROM tasks WHERE {TASK_DESCRIPTION} = %s
                    """,(desc,))
                    
            # checks how many rows were deleted and prints it
            deleted_tasks_number = self.cursor.rowcount
            print(f"Deleted {deleted_tasks_number} task(s) with description '{desc}'.")
        except Exception as e:
            print(f"Error deleting task by desc: {e}")
            #if there was an error rollback the deletions
            self.connection.rollback()

        self.connection.commit()

    def update_task(self, task_id, task_uid, task_list=None, new_desc=None, new_status=None, new_alarm_time=None, new_due_date=None):
        query = []
        params = []
    
        if new_desc is not None:
            query.append(f"{TASK_DESCRIPTION} = %s")
            params.append(new_desc)
        if new_status is not None:
            query.append(f"{TASK_IS_COMPLETED} = %s")
            params.append(new_status)
        if new_alarm_time is not None:
            params.append(new_alarm_time.astimezone(pytz.UTC) if isinstance(new_alarm_time, datetime) else datetime.fromisoformat(new_alarm_time).astimezone(pytz.UTC))
            query.append(f"{TASK_ALARM_TIME} = %s")
        if new_due_date is not None:
            params.append(new_due_date.astimezone(pytz.UTC) if isinstance(new_due_date, datetime) else datetime.fromisoformat(new_due_date).astimezone(pytz.UTC))
            query.append(f"{TASK_DUE_DATE} = %s")
        if task_list is not None:
            query.append(f"{TASK_LIST} = %s")
            params.append(task_list)
    
        if query:
            params.extend([task_id, task_uid])
            query = f"UPDATE tasks SET {', '.join(query)} WHERE {TASK_PRIMARY_KEY} = %s AND {TASK_UID} = %s"

            try:
                self.cursor.execute(query, tuple(params))
                self.connection.commit()
                print("Task updated successfully.")
            except Exception as e:
                print(f"Error updating task: {e}")
                self.connection.rollback()
        else:
            print("No fields to update provided.")

    def delete_task_alarm_by_id(self, task_id, task_uid):
        query = f"UPDATE tasks SET {TASK_ALARM_TIME} = NULL WHERE {TASK_PRIMARY_KEY} = %s AND {TASK_UID} = %s"
        values = (task_id, task_uid)
        
        try:
            self.cursor.execute(query, values)
            self.connection.commit()
            print("Alarm deleted successfully.")
        except Exception as e:
            print(f"Error resetting alarm: {e}")
            self.connection.rollback()
    
    def delete_task_due_date_by_id(self, task_id, task_uid):
        query = f"UPDATE tasks SET {TASK_DUE_DATE} = NULL WHERE {TASK_PRIMARY_KEY} = %s AND {TASK_UID} = %s"
        values = (task_id, task_uid)
        
        try:
            self.cursor.execute(query, values)
            self.connection.commit()
            print("Due date deleted successfully.")
        except Exception as e:
            print(f"Error resetting alarm: {e}")
            self.connection.rollback()



    def __del__(self):
        print("Closing connection")
        self.connection.close()

## Test Case 1: Create a Task
task_db = TaskDatabase(host='localhost', dbname='minmax', user='postgres', password='dog', port=5432)

# task_db.delete_all_tasks()

#print("Testing task creation...")
#task_db.create_task(
#    task_uid="1234",
#    task_list="Work",
#    task_desc="Finish the report",
#    task_alarm_time=datetime(2024, 11, 7, 14, 30, tzinfo=pytz.UTC),
#    task_due_date=datetime(2024, 12, 7, 14, 30, tzinfo=pytz.UTC)
#)
#
### Test Case 2: Read All Tasks for a given UID
#print("\nTesting reading tasks by UID...")
#tasks = task_db.read_all_tasks("1234")
#print(f"Tasks for UID '1234': {tasks}")
#
#task_db.update_task(
#    task_id=13,
#    task_uid="1234",
#    task_list="Work",
#    new_due_date=datetime(2024, 11, 7, 14, 30, tzinfo=pytz.UTC)
#)

#print("\nTesting reading tasks by UID after alarm")
#tasks = task_db.read_all_tasks("1234")
#print(f"Tasks for UID '1234': {tasks}")
## Test Case 3: Read Task by Task ID
#print("\nTesting reading a task by task ID...")
#task = task_db.read_at_task_id(1)  # Assuming the first task has ID 1
#print(f"Task with ID 1: {task}")