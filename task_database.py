import firebase_admin
from firebase_admin import credentials, auth, firestore

# Path to your Firebase private key file
cred = credentials.Certificate("/Users/pujitha/Downloads/to-do-list.json")
firebase_admin.initialize_app(cred)

import psycopg2
from datetime import datetime, timedelta

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
USER_ID = "user_id"




class TaskDatabase:

    @staticmethod
    def verify_user_token(id_token):
        try:
            decoded_token = auth.verify_id_token(id_token)
            user_id = decoded_token['uid']  # This user ID can be stored in your PostgreSQL tasks table
            return user_id
        except Exception as e:
            print(f"Error verifying user token: {e}")
            return None

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
                    {USER_ID} VARCHAR(255)
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
    

    def create_task(self, task_desc):
        """
        Creates basic task which is automatically set to false completed. Needs time implementation.
        """

        try:
            self.cursor.execute(f"""
                INSERT INTO tasks({TASK_DESCRIPTION}, {TASK_IS_COMPLETED}, {TASK_CREATED_TIME_STAMP})
                VALUES(%s, %s, CURRENT_TIMESTAMP);
            """, (task_desc, False))
            print("Task created.")

        except Exception as e:
            print(f"Error creating task: {e}")
            self.connection.rollback()
        
        self.connection.commit()

    
    def create_user_task(self, task_desc, user_id=None):
        """
        Creates task for a specific user.
        """

        try:
            self.cursor.execute(f"""
                INSERT INTO tasks({TASK_DESCRIPTION}, {TASK_IS_COMPLETED}, {TASK_CREATED_TIME_STAMP}, {USER_ID})
                VALUES(%s, %s, CURRENT_TIMESTAMP, %s);
            """, (task_desc, False, user_id))
            print("Task created.")

        except Exception as e:
            print(f"Error creating task: {e}")
            self.connection.rollback()
        
        self.connection.commit()


    def read_all_tasks(self):
        """Reads all tasks in list for a specific user."""

        try:
            self.cursor.execute(f"""
                SELECT * FROM tasks;
            """)
            all_tasks = self.cursor.fetchall()
            return all_tasks
        
        except Exception as e:
            print(f"Error reading tasks: {e}")
    

    def read_user_tasks(self, user_id=None):
        """Reads all tasks in list for a specific user."""

        try:
            self.cursor.execute(f"""
                SELECT * FROM tasks WHERE {USER_ID} = %s;
            """, (user_id))
            all_tasks = self.cursor.fetchall()
            return all_tasks
        
        except Exception as e:
            print(f"Error reading tasks: {e}")


    def read_at_task_id(self, index):
        """Reads task at index"""

        try:
            self.cursor.execute(f"""
                SELECT * FROM tasks WHERE {TASK_PRIMARY_KEY} = %s;
            """, (index))
            task = self.cursor.fetchone()
            return task
        
        except Exception as e:
            print(f"Error reading task: {e}")


    def read_user_task_id(self, index, user_id=None):
        """Reads task at index for a specific user."""

        try:
            self.cursor.execute(f"""
                SELECT * FROM tasks WHERE {TASK_PRIMARY_KEY} = %s AND {USER_ID} = %s;
            """, (index, user_id))
            task = self.cursor.fetchone()
            return task
        
        except Exception as e:
            print(f"Error reading task: {e}")


    def read_tasks_with_status(self, status):
        """
        Reads all tasks with an is completed status set to either (True or False)

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
    

    def read_user_tasks_with_status(self, status, user_id):
        """
        Reads all tasks with an is completed status set to either (True or False) for a specific user

        """
        try:
            self.cursor.execute(f"""
                    SELECT * FROM tasks WHERE {TASK_IS_COMPLETED} = {status} AND {USER_ID} = %s;
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
            self.connection.rollback()


    def delete_task_by_index(self,index):
        """
        Deletes a task from the database using the index
        """
        try:
            # fetches task  useing %s to only catch string type arguments 
            self.cursor.execute(f"""
                SELECT * FROM tasks WHERE {TASK_PRIMARY_KEY} = %s
                """, (index))
            task = self.cursor.fetchone()

            #if task found delete otherwise print not found
            if task:
                print(f"Deleting task: {task}")

                self.cursor.execute(f"""
                    DELETE FROM tasks WHERE {TASK_PRIMARY_KEY} = %s 
                    """,(index))
            else:
                print(f"No task found with index: {index}")
        except Exception as e:
            print(f"Error deleting task by index: {e}")
            self.connection.rollback()

        self.connection.commit()


    def delete_user_task_by_index(self,index, user_id=None):
        """
        Deletes a task from a specific user using the index
        """
        try:
            # fetches task  useing %s to only catch string type arguments 
            self.cursor.execute(f"""
                SELECT * FROM tasks WHERE {TASK_PRIMARY_KEY} = %s AND {USER_ID} = %s
                """, (index, user_id))
            task = self.cursor.fetchone()

            #if task found delete otherwise print not found
            if task:
                print(f"Deleting task: {task}")

                self.cursor.execute(f"""
                    DELETE FROM tasks WHERE {TASK_PRIMARY_KEY} = %s AND {USER_ID} = %s
                    """,(index, user_id))
            else:
                print(f"No task found with index: {index}")

        except Exception as e:
            print(f"Error deleting task by index: {e}")
            self.connection.rollback()

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

    def update_task(self, task_id, new_desc=None, new_status=None):
        """Updates a task's description, status, or both based on the task_id"""
        try:
            if new_desc is not None and new_status is not None:
                self.cursor.execute(f"""
                    UPDATE tasks
                    SET {TASK_DESCRIPTION} = %s, {TASK_IS_COMPLETED} = %s
                    WHERE {TASK_PRIMARY_KEY} = %s;
                """, (new_desc, new_status, task_id))
            elif new_desc is not None:
                self.cursor.execute(f"""
                    UPDATE tasks
                    SET {TASK_DESCRIPTION} = %s
                    WHERE {TASK_PRIMARY_KEY} = %s;
                """, (new_desc, task_id))
            elif new_status is not None:
                self.cursor.execute(f"""
                    UPDATE tasks
                    SET {TASK_IS_COMPLETED} = %s
                    WHERE {TASK_PRIMARY_KEY} = %s;
                """, (new_status, task_id))
            else:
                print("No changes specified for update.")
                return
            
            self.connection.commit()
            print(f"Task with ID {task_id} updated successfully.")

        except Exception as e:
            print(f"Error updating task with ID {task_id}: {e}")
            self.connection.rollback()


    def update_user_task(self, task_id, new_desc=None, new_status=None, user_id=None):
        """Updates a task's description, status, or both based on the task_id for a specific user."""
        try:
            if new_desc is not None and new_status is not None:
                self.cursor.execute(f"""
                    UPDATE tasks
                    SET {TASK_DESCRIPTION} = %s, {TASK_IS_COMPLETED} = %s
                    WHERE {TASK_PRIMARY_KEY} = %s AND {USER_ID} = %s;
                """, (new_desc, new_status, task_id, user_id))
            elif new_desc is not None:
                self.cursor.execute(f"""
                    UPDATE tasks
                    SET {TASK_DESCRIPTION} = %s
                    WHERE {TASK_PRIMARY_KEY} = %s AND {USER_ID} = %s;
                """, (new_desc, task_id, user_id))
            elif new_status is not None:
                self.cursor.execute(f"""
                    UPDATE tasks
                    SET {TASK_IS_COMPLETED} = %s
                    WHERE {TASK_PRIMARY_KEY} = %s AND {USER_ID} = %s;
                """, (new_status, task_id, user_id))
            else:
                print("No changes specified for update.")
                return
            
            self.connection.commit()
            print(f"Task with ID {task_id} updated successfully.")

        except Exception as e:
            print(f"Error updating task with ID {task_id}: {e}")
            self.connection.rollback()

    def get_tasks_created_last_week(self, user_id):
        """Gets the count of tasks created in the last week for a specific user."""

        try:
            last_week = datetime.now() - timedelta(days=7)
            self.cursor.execute(f"""
                SELECT COUNT(*) FROM tasks 
                WHERE {USER_ID} = %s AND {TASK_CREATED_TIME_STAMP} >= %s;
            """, (user_id, last_week))
            created_count = self.cursor.fetchone()[0]
            return created_count
        
        except Exception as e:
            print(f"Error fetching tasks created in last week: {e}")
            return None

    def get_tasks_completed_last_week(self, user_id):
        """Gets the count of tasks completed in the last week for a specific user."""

        try:
            last_week = datetime.now() - timedelta(days=7)
            self.cursor.execute(f"""
                SELECT COUNT(*) FROM tasks 
                WHERE {USER_ID} = %s AND {TASK_IS_COMPLETED} = TRUE 
                AND {TASK_CREATED_TIME_STAMP} >= %s;
            """, (user_id, last_week))
            completed_count = self.cursor.fetchone()[0]
            return completed_count
        
        except Exception as e:
            print(f"Error fetching tasks completed in last week: {e}")
            return None
        
    def get_tasks_created_and_completed_week(self, user_id, start_date):
        """Gets counts of tasks created and completed in a given week for a specific user."""

        try:
            end_date = start_date + timedelta(days=7)

            # Tasks created in the specified week
            self.cursor.execute(f"""
                SELECT COUNT(*) FROM tasks 
                WHERE {USER_ID} = %s AND {TASK_CREATED_TIME_STAMP} >= %s 
                AND {TASK_CREATED_TIME_STAMP} < %s;
            """, (user_id, start_date, end_date))
            created_count = self.cursor.fetchone()[0]

            # Tasks completed in the specified week
            self.cursor.execute(f"""
                SELECT COUNT(*) FROM tasks 
                WHERE {USER_ID} = %s AND {TASK_IS_COMPLETED} = TRUE 
                AND {TASK_CREATED_TIME_STAMP} >= %s AND {TASK_CREATED_TIME_STAMP} < %s;
            """, (user_id, start_date, end_date))
            completed_count = self.cursor.fetchone()[0]

            return {"tasks_created": created_count, "tasks_completed": completed_count}
        
        except Exception as e:
            print(f"Error fetching tasks for week starting on {start_date}: {e}")
            return None


    def get_tasks_created_last_month(self, user_id):
        """Gets the count of tasks created in the last month for a specific user."""

        try:
            last_month = datetime.now() - timedelta(days=30)
            self.cursor.execute(f"""
                SELECT COUNT(*) FROM tasks 
                WHERE {USER_ID} = %s AND {TASK_CREATED_TIME_STAMP} >= %s;
            """, (user_id, last_month))
            task_count = self.cursor.fetchone()[0]
            return task_count
        
        except Exception as e:
            print(f"Error fetching tasks created in last month: {e}")
            return None
        
    def get_tasks_completed_last_month(self, user_id):
        """Gets the count of tasks completed in the last month for a specific user."""

        try:
            last_month = datetime.now() - timedelta(days=30)
            self.cursor.execute(f"""
                SELECT COUNT(*) FROM tasks 
                WHERE {USER_ID} = %s AND {TASK_IS_COMPLETED} = TRUE 
                AND {TASK_CREATED_TIME_STAMP} >= %s;
            """, (user_id, last_month))
            completed_count = self.cursor.fetchone()[0]
            return completed_count
        
        except Exception as e:
            print(f"Error fetching tasks completed in last month: {e}")
            return None
        
    def get_tasks_created_and_completed_month(self, user_id, month, year):
        """Gets counts of tasks created and completed in a given month for a specific user."""

        try:
            start_date = datetime(year, month, 1)
            end_date = (start_date + timedelta(days=31)).replace(day=1)  # First day of the next month
            
            # Tasks created in the specified month
            self.cursor.execute(f"""
                SELECT COUNT(*) FROM tasks 
                WHERE {USER_ID} = %s AND {TASK_CREATED_TIME_STAMP} >= %s 
                AND {TASK_CREATED_TIME_STAMP} < %s;
            """, (user_id, start_date, end_date))
            created_count = self.cursor.fetchone()[0]

            # Tasks completed in the specified month
            self.cursor.execute(f"""
                SELECT COUNT(*) FROM tasks 
                WHERE {USER_ID} = %s AND {TASK_IS_COMPLETED} = TRUE 
                AND {TASK_CREATED_TIME_STAMP} >= %s AND {TASK_CREATED_TIME_STAMP} < %s;
            """, (user_id, start_date, end_date))
            completed_count = self.cursor.fetchone()[0]

            return {"tasks_created": created_count, "tasks_completed": completed_count}
        except Exception as e:
            print(f"Error fetching tasks for month {month}/{year}: {e}")
            return None


    






#minmax_database = TaskDatabase("localhost", "to_do_list", "postgres", "dog", 5433)
#minmax_database.create_task("Test")
#minmax_database.create_task("Dog")
#minmax_database.update_task(11, "Cat", True)
#print(minmax_database.read_all_tasks())
#minmax_database.delete_all_tasks()

#minmax_database = TaskDatabase("localhost", "minmax", "postgres", "dog", 5432)
#minmax_database.create_task("Test")
#minmax_database.create_task("Dog")
#listTest = minmax_database.read_tasks_with_status(False)
#
#
#
#for x in listTest:
#    print(x)
