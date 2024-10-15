import psycopg2

connection = psycopg2.connect(host="localhost", dbname = "postgres", user="postgres", password="dog", port = 5432)


cursor = connection.cursor();


cursor.execute("""CREATE TABLE IF NOT EXISTS person( 
                id INT PRIMARY KEY,
                name VARCHAR(255),
                age INT,
                gender CHAR
            )
            
            """)



connection.commit()

cursor.close()
connection.close()

