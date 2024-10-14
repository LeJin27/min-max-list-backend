import mysql.connector


class DataBases():
    def __init__(self, db_name, db_table):
        self.db_table = db_table
        
        self.connection = mysql.connector.connect(user='root', password='db-root', database=db_name)
        self.cursor = self.connection.cursor(dictionary=True)


    ### get this to return a struct
    def test_query(self):
        query = ("SELECT * FROM Tasks")
        self.cursor.execute(query)
        for row in self.cursor:
            print(row)
    

    def print_open_tasks(self):
        query = ("SELECT * FROM Tasks where status = 'open'")
        self.cursor.execute(query)
        for row in self.cursor:
            print(row)


    def print_close_tasks(self):
        query = ("SELECT * FROM Tasks where status = 'close'")
        self.cursor.execute(query)
        for row in self.cursor:
            print(row)
    
    def create_tasks(self, id, name, status):
        add_employee = ("INSERT INTO employees "
               "(first_name, last_name, hire_date, gender, birth_date) "
               "VALUES (%s, %s, %s, %s, %s)")




    
    
    

    



    


p1 = DataBases('todo', 'tasks')
p1.create_tasks(20, "dog", "open")
p1.print_open_tasks()