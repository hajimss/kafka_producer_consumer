import mysql.connector

try:
    mydb = mysql.connector.connect(
        user="root",
        host="localhost",
        password="password",
        database="kafkadb"
    )

except mysql.connector.Error as err:
    print("Failed to connect: {}".format(err))

def new_user(ID, FirstName, LastName, Age):
    #method POST
    mysql_insert_query = """INSERT INTO Persons (ID, FirstName, LastName, Age)
                                VALUES
                                ({}, '{}', '{}', {})""".format(ID, FirstName, LastName, Age)
    #print(mysql_insert_query)
    cur = mydb.cursor()
    cur.execute(mysql_insert_query)
    mydb.commit()

    response = "New entry ({}, '{}', '{}', {}) inserted".format(ID, FirstName, LastName, Age)
    return response

def view_all(table):
    #method GET
    cur = mydb.cursor()
    cur.execute("SELECT * FROM {}".format(table))
    response = list(cur.fetchall())
#    response = ''
#    for x in result:
#        response = response + str(x)
#        print(x)
    return response

def delete_user(id):
    mysql_delete_query = "DELETE FROM Persons where ID = {}".format(id)
    cur = mydb.cursor()
    cur.execute(mysql_delete_query)
    mydb.commit()
    return (str(cur.rowcount) + " record(s) deleted")


    
