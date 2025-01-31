import psycopg2
import chardet

# Database connection parameters
db_name = "chinook"
user = "postgres"
password = "welcome"
host = "localhost"
port = "5432"

# Path to the SQL file
sql_file_path = 'Chinook_PostgreSql.sql'

# Function to check encoding
def check_encoding(file_path):
    rawdata = open(file_path, 'rb').read()
    result = chardet.detect(rawdata)
    return result['encoding']

# Check encoding of the SQL file
encoding = check_encoding(sql_file_path)
print(f"File encoding: {encoding}")

# Read the SQL file with the detected encoding
with open(sql_file_path, 'r', encoding=encoding) as file:
    sql_commands = file.read()

# Connect to PostgreSQL database
conn = psycopg2.connect(dbname=db_name, user=user, password=password, host=host, port=port)
cur = conn.cursor()

# Execute the SQL commands
cur.execute(sql_commands)

# Commit and close the connection
conn.commit()
cur.close()
conn.close()

print("SQL file executed successfully.")
