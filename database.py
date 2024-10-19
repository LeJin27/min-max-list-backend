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
        Creates basic task which is automatically set to true. Needs time implementation.
        """

        try:
            self.cursor.execute(f"""
                    insert into tasks(task_desc,task_is_open, created_time_stamp) 
                    values('{task_desc}', True, CURRENT_TIMESTAMP)
                    """);
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


    
        


test = TaskDatabase("localhost", "minmax", "postgres", "dog", 5432)
print(test.read_all_is_open_task(True))














