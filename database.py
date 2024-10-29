import psycopg2


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
                self.connection = psycopg2.connect(host=self.host, dbname = self.dbname, user=self.user, password=self.password, port = self.port)
                self.cursor = self.connection.cursor()
            else: 
                print("Something really went wrong")
        

        # Creating Table of Tasks
        print("Creating tasks table")
        self.connection.autocommit = True  
        try:
            self.cursor.execute("""
                    CREATE TABLE IF NOT EXISTS tasks (
                    task_id SERIAL PRIMARY KEY, 
                    task_desc VARCHAR(255), 
                    task_is_open BOOLEAN,
                    created_time_stamp TIMESTAMPTZ
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
        Creates basic task which automatically: sets open = true 
        and has a timestamp for when it was created
        """

        try:
            self.cursor.execute(f"""
                    insert into tasks(task_desc,task_is_open, created_time_stamp) 
                    values('{task_desc}', True, CURRENT_TIMESTAMP)
                    """);
        except Exception as e:
            print(f"Error creating task: {e}")
        
        self.connection.commit()

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
            self.cursor.execute("""
                SELECT * FROM tasks WHERE task_id = %s
                """, (index,))
            task = self.cursor.fetchone()

            #if task found delete otherwise print not found
            if task:
                print(f"Deleting task: {task}")

                self.cursor.execute(f"""
                    DELETE FROM tasks WHERE task_id = %s 
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
                    DELETE FROM tasks WHERE task_desc = %s
                    """,(desc,))
                    
            # checks how many rows were deleted and prints it
            deleted_tasks_number = self.cursor.rowcount
            print(f"Deleted {deleted_tasks_number} task(s) with description '{desc}'.")
        except Exception as e:
            print(f"Error deleting task by desc: {e}")
            #if there was an error rollback the deletions
            self.connection.rollback()

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

    def read_at_task(self, index):
        """
        Reads task at index i
        """
        try:
            self.cursor.execute(f"""
                    SELECT * FROM tasks WHERE task_id = {index}
                    """);
        except Exception as e:
            print(f"Error reading task: {e}")
        
        self.connection.commit()

        all_tasks = self.cursor.fetchall()
        return all_tasks

    def read_all_is_open_task(self, status):
        """
        Reads all tasks with an is open status set to either (True or False)
        """
        try:
            self.cursor.execute(f"""
                    SELECT * FROM tasks WHERE task_is_open = {status}
                    """);

        except Exception as e:
            print(f"Error reading task: {e}")
        
        self.connection.commit()
        all_tasks = self.cursor.fetchall()
        return all_tasks
    
    def __del__(self):
        print("Closing connection")
        self.connection.close()


    
        


test = TaskDatabase("localhost", "minmax", "postgres", "dog", 5432)

test.delete_all_tasks()
test.create_task("Task 1")
test.create_task("Task 2")
test.create_task("Task 3")
test.delete_task_by_index(1)
test.delete_task_by_desc("Task 2")


print(test.read_all_is_open_task(True))














