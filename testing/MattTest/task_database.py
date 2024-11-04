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
TASK_DESCRIPTION = "task_desc"
TASK_IS_COMPLETED = "task_is_completed"
TASK_CREATED_TIME_STAMP = "task_created_time_stamp"
TASK_ALARM_TIME = "task_alarm_time"




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
                    {TASK_DESCRIPTION} VARCHAR(255), 
                    {TASK_IS_COMPLETED} BOOLEAN,
                    {TASK_CREATED_TIME_STAMP} TIMESTAMPTZ,
                    {TASK_ALARM_TIME} TIMESTAMPTZ
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
    

    
    def create_task(self, task_desc, task_alarm_time=None):
        """
        Creates basic task which is automatically set to false completed. Needs time implementation.
        """
        print(f"Task Alarm Time: {task_alarm_time}, Type: {type(task_alarm_time)}")

        try:
            # check if alarm is string or datetime and handle appropiately
            if task_alarm_time:
                if isinstance(task_alarm_time, str):
                    task_alarm_time = datetime.fromisoformat(task_alarm_time)

                if isinstance(task_alarm_time,datetime):
                    task_alarm_time = task_alarm_time.astimezone(pytz.UTC)


            self.cursor.execute(f"""
                INSERT INTO tasks({TASK_DESCRIPTION}, {TASK_IS_COMPLETED}, {TASK_CREATED_TIME_STAMP},{TASK_ALARM_TIME})
                VALUES(%s, %s, CURRENT_TIMESTAMP,%s);
            """, (task_desc, False, task_alarm_time))
        except Exception as e:
            print(f"Error creating task: {e}")
        
        self.connection.commit()

    
    def read_all_tasks(self):
        """
        Reads all tasks in list
        """
        try:
            self.cursor.execute(f"""
                    select * from tasks
                    """);
        except Exception as e:
            print(f"Error reading task: {e}")
        
        self.connection.commit()

        all_tasks = self.cursor.fetchall()
        return all_tasks

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

    def read_tasks_with_status(self, status):
        """
        Reads all tasks with an is open status set to either (True or False)

        """
        try:
            self.cursor.execute(f"""
                    SELECT * FROM tasks WHERE {TASK_IS_COMPLETED} = {status}
                    """);

        except Exception as e:
            print(f"Error reading task: {e}")
        
        self.connection.commit()
        all_tasks = self.cursor.fetchall()
        return all_tasks


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
    
    def __del__(self):
        print("Closing connection")
        self.connection.close()

    def update_task(self, task_id, new_desc=None, new_status=None,new_alarm_time=None):
        """
        Updates a task's description, status, or both based on the task_id.
        """
        try:
            # Update both description and status if both are provided
            if new_desc is not None and new_status is not None and new_alarm_time is not None:
                self.cursor.execute(f"""
                    UPDATE tasks
                    SET {TASK_DESCRIPTION} = %s, {TASK_IS_COMPLETED} = %s, {TASK_ALARM_TIME} = %s
                    WHERE {TASK_PRIMARY_KEY} = %s
                    """, (new_desc, new_status,new_alarm_time, task_id))
            
            elif new_desc is not None and new_status is not None:
                self.cursor.execute(f"""
                    UPDATE tasks
                    SET {TASK_DESCRIPTION} = %s, {TASK_IS_COMPLETED} = %s
                    WHERE {TASK_PRIMARY_KEY} = %s
                    """, (new_desc, new_status, task_id))
                
            elif new_desc is not None and new_alarm_time is not None:
                self.cursor.execute(f"""
                    UPDATE tasks
                    SET {TASK_DESCRIPTION} = %s, {TASK_ALARM_TIME} = %s
                    WHERE {TASK_PRIMARY_KEY} = %s
                    """, (new_desc, new_alarm_time, task_id))
                
            elif new_alarm_time is not None and new_status is not None:
                self.cursor.execute(f"""
                    UPDATE tasks
                    SET {TASK_ALARM_TIME} = %s, {TASK_IS_COMPLETED} = %s
                    WHERE {TASK_PRIMARY_KEY} = %s
                    """, (new_alarm_time, new_status, task_id))
            
            # Update only the description if provided
            elif new_desc is not None:
                self.cursor.execute(f"""
                    UPDATE tasks
                    SET {TASK_DESCRIPTION} = %s
                    WHERE {TASK_PRIMARY_KEY} = %s
                    """, (new_desc, task_id))
            
            # Update only the status if provided
            elif new_status is not None:
                self.cursor.execute(f"""
                    UPDATE tasks
                    SET {TASK_IS_COMPLETED} = %s
                    WHERE {TASK_PRIMARY_KEY} = %s
                    """, (new_status, task_id))
            
            elif new_alarm_time is not None:
                self.cursor.execute(f"""
                    UPDATE tasks
                    SET {TASK_ALARM_TIME} = %s
                    WHERE {TASK_PRIMARY_KEY} = %s
                    """, (new_alarm_time, task_id))
            
            else:
                print("No changes specified for update.")
                return
            
            # Commit the transaction and print success message
            self.connection.commit()
            print(f"Task with ID {task_id} updated successfully.")

        except Exception as e:
            # Handle any errors and rollback changes if necessary
            print(f"Error updating task with ID {task_id}: {e}")
            self.connection.rollback()





#minmax_database = TaskDatabase("localhost", "minmax", "postgres", "dog", 5432)
#minmax_database.create_task("Test","2024-11-04T09:00:00+00:00")
#minmax_database.create_task("Dog")
#minmax_database.update_task(2,None,None,"2024-11-04T09:10:00+00:00")
#listTest = minmax_database.read_tasks_with_status(False)
#for x in listTest:
#    print(x)

    
        
















