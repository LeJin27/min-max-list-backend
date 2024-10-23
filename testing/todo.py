import psycopg2

# Connect to PostgreSQL database
try:
    conn = psycopg2.connect(
        dbname="to_do_list",  
        user="postgres",       
        password="dog", 
        host="localhost",       
        port="5433"             
    )
    cur = conn.cursor()
    print("Connected to the database successfully!")

    # Create the 'task' table if it doesn't exist
    create_table_query = """
    CREATE TABLE IF NOT EXISTS task (
        id SERIAL PRIMARY KEY,         -- Unique ID for each task
        title VARCHAR(255) NOT NULL,   -- Task title
        description TEXT,              -- Task description (optional)
        status VARCHAR(50) NOT NULL DEFAULT 'pending', -- Task status
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,  -- Creation time
        due_date TIMESTAMP             -- Optional due date for the task
    );
    """
    cur.execute(create_table_query)
    conn.commit()
    print("Table 'task' is ready!")

    # Create a task
    def create_task(title, description, status, due_date):
        try:
            query = """
            INSERT INTO task (title, description, status, due_date)
            VALUES (%s, %s, %s, %s);
            """
            cur.execute(query, (title, description, status, due_date))
            conn.commit()
            print("Task added successfully!")
        except Exception as e:
            print(f"Error inserting task: {e}")

    # Get tasks
    def get_tasks():
        try:
            query = "SELECT * FROM task;"
            cur.execute(query)
            tasks = cur.fetchall()
            for task in tasks:
                print(task)
        except Exception as e:
            print(f"Error fetching tasks: {e}")

    # Update task status
    def update_task_status(task_id, new_status):
        try:
            query = "UPDATE task SET status = %s WHERE id = %s;"
            cur.execute(query, (new_status, task_id))
            conn.commit()
            print("Task updated successfully!")
        except Exception as e:
            print(f"Error updating task: {e}")

    # Delete a task
    def delete_task(task_id):
        try:
            query = "DELETE FROM task WHERE id = %s;"
            cur.execute(query, (task_id,))
            conn.commit()
            print("Task deleted successfully!")
        except Exception as e:
            print(f"Error deleting task: {e}")

    # Call CRUD functions for testing
    create_task("Learn Python", "Complete Python tutorials", "pending", "2024-10-20")
    get_tasks()
    update_task_status(1, "completed")
    delete_task(1)

    # Close connection
    cur.close()
    conn.close()
    print("Database connection closed.")

except Exception as e:
    print(f"Error connecting to the database: {e}")
