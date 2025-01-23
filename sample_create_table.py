import psycopg2

def create_employee_table(host, database, user, password):
    try:
        # Establish the connection
        conn = psycopg2.connect(
            host=host,
            database=database,
            user=user,
            password=password
        )
        cursor = conn.cursor()
        
        # Create employee table
        create_table_query = '''
        CREATE TABLE IF NOT EXISTS employee (
            id SERIAL PRIMARY KEY,
            name VARCHAR(100),
            age INTEGER,
            department VARCHAR(50)
        )
        '''
        cursor.execute(create_table_query)
        conn.commit()
        
        # Sample data
        employees = [
            {"name": "John Doe", "age": 30, "department": "HR"},
            {"name": "Jane Smith", "age": 25, "department": "Finance"},
            {"name": "Emily Davis", "age": 35, "department": "IT"},
            {"name": "Michael Brown", "age": 40, "department": "Management"},
            {"name": "Jessica Wilson", "age": 28, "department": "Marketing"},
            {"name": "Daniel Taylor", "age": 32, "department": "Sales"},
            {"name": "Laura Moore", "age": 29, "department": "Support"},
            {"name": "James Anderson", "age": 45, "department": "Operations"},
            {"name": "Sarah Thomas", "age": 31, "department": "Development"},
            {"name": "David Jackson", "age": 27, "department": "Design"}
        ]
        
        # Insert sample data
        for emp in employees:
            insert_query = '''
            INSERT INTO employee (name, age, department) VALUES (%s, %s, %s)
            '''
            cursor.execute(insert_query, (emp["name"], emp["age"], emp["department"]))
        
        conn.commit()
        
        # Close the connection
        cursor.close()
        conn.close()
        
        print("Employee table created and sample data inserted successfully.")
    except Exception as e:
        print(f"Error: {e}")

# Example usage
if __name__ == "__main__":
    host = "localhost"
    database = ""
    user = ""
    password = ""
    
    create_employee_table(host, database, user, password)