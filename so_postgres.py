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

    # cursor.execute(query)
    
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

##### laptop code ##############

# import psycopg2

# # Connect to the PostgreSQL database
# conn = psycopg2.connect(
#     host="localhost",
#     port=5432,
#     database="stackoverflow",
#     user="root",
#     password="12345"
# )

# # Create a cursor object
# cur = conn.cursor()

# #automatically fetch snapshot data in postgress db
# #hey and ty! please crete a script that will take the questions and only the answers written in code from the following table : 

# # Execute a sample query
# cur.execute("SELECT * from cars;")
# version = cur.fetchall()#[0]
# print(f"Tables in DB: {version}")

# # Close the cursor and connection
# cur.close()
# conn.close()

##### laptop code ##############