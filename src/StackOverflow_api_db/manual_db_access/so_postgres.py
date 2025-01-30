import psycopg2


def get_so_postgres_question():
    # Establish a connection to the PostgreSQL database
    connection = psycopg2.connect(
        host="localhost",
        port="5432",
        database="stackoverflow",
        user="root",
        password="12345"
    )

    # Create a cursor object
    cursor = connection.cursor()

    # Execute your SQL query
    query = "SELECT * FROM delet;"

    #get question
    # query = "SELECT body FROM posts WHERE id = 4;" 

    cursor.execute(query)

    # Fetch all the rows returned by the query
    rows = cursor.fetchall()
    #print(f"Tables in DB: {rows}")

    # Close the cursor and connection
    cursor.close()
    connection.close()    
    
    # Process the rows as needed
    result = ""
    for row in rows:
        result += str(row) + "\n"
    
    return result