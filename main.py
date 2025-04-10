import pymysql

# Database configuration
db_config = {
    'user': 'root',
    'password': 'tanvi.G@164',
    'host': '127.0.0.1',
    'database': 'expense_tracker'
}

# Connect to the database
def connect_to_mysql():
    """Establish MySQL connection."""
    return pymysql.connect(**db_config)

def test_connection():
    try:
        conn = connect_to_mysql()
        print("Connection successful")
    except pymysql.MySQLError as e:
        print(f"Connection error: {e}")
    finally:
        conn.close()

test_connection()