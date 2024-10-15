import psycopg2


"""
Used to create a data for all todo related functions 

create_table 
create_task  //create task given properties 
drop_task //drop tasks with a given id
---
Different queries
---
get_task_done
get_task_not_done
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
                self.create_database()
            else: 
                print("Something really went wrong")
        

        # Creating table
        print("Creating tasks table")
        try:
            self.cursor.execute("CREATE TABLE IF NOT EXISTS tasks (task_id SERIAL PRIMARY KEY, task_desc VARCHAR(255), task_is_open BOOLEAN);")
        except Exception as e:
            print("Something when wrong")

        self.connection.commit()
    

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


    
        


test = TaskDatabase("localhost", "minmax", "postgres", "dog", 5432)














