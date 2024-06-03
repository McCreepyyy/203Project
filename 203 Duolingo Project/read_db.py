
import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect('test.db')
c = conn.cursor()

# Execute a SQL query to get all users from the 'user' table
c.execute('SELECT * FROM user')

# Fetch all the rows from the query
rows = c.fetchall()

# Print each row
for row in rows:
    print(row)

# Close the connection to the database
conn.close()