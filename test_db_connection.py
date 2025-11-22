import pymysql
import sys

def test_connection():
    print("Attempting to connect to MySQL at localhost:3306...")
    try:
        # Connect to the server (no database selected yet)
        connection = pymysql.connect(
            host='localhost',
            user='root',
            password='',
            port=3306,
            cursorclass=pymysql.cursors.DictCursor
        )
        print("SUCCESS: Connected to MySQL server!")
        
        try:
            with connection.cursor() as cursor:
                # Check if 'fixit' database exists
                cursor.execute("SHOW DATABASES LIKE 'bybytoo'")
                result = cursor.fetchone()
                if result:
                    print("Database 'bybytoo' exists.")
                else:
                    print("Database 'bybytoo' does not exist. Creating it...")
                    cursor.execute("CREATE DATABASE bybytoo")
                    print("SUCCESS: Database 'bybytoo' created.")
        finally:
            connection.close()
            
    except pymysql.err.OperationalError as e:
        print(f"ERROR: Could not connect to MySQL. Details: {e}")
        print("\nTroubleshooting tips:")
        print("1. Check XAMPP Control Panel: Is the 'MySQL' module green/running?")
        print("2. Check Port: Is MySQL running on port 3306? (Look at the 'Port' column in XAMPP)")
        print("3. Check Password: Does your 'root' user have a password? (Default XAMPP has none)")
        sys.exit(1)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        sys.exit(1)

if __name__ == "__main__":
    test_connection()
