import sqlite3

connection_obj = sqlite3.connect('users.db')
 
# cursor object
cursor_obj = connection_obj.cursor()
 
# Drop the GEEK table if already exists.
cursor_obj.execute("DROP TABLE IF EXISTS GEEK")
 
# Creating table
table = """ CREATE TABLE users (
  id SERIAL PRIMARY KEY,
  name VARCHAR(255) NOT NULL,
  email VARCHAR(255) NOT NULL,
  phone NUM NOT NULL,
  password VARCHAR(255) NOT NULL
); """
 
cursor_obj.execute(table)
 
print("Table is Ready")
 
# Close the connection
connection_obj.close()