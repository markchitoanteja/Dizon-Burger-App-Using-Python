import mysql.connector

class DatabaseManager:
    def __init__(self):
        self.config = {
            'user': 'root',
            'password': '',
            'host': 'localhost'
        }
        self.db_name = 'burger_app'
        self.table_name = 'users'
        self.init_database()

    def init_database(self):
        try:
            conn = mysql.connector.connect(**self.config)
            cursor = conn.cursor()
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS {self.db_name}")
            conn.database = self.db_name

            cursor.execute(f'''
                CREATE TABLE IF NOT EXISTS {self.table_name} (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    name VARCHAR(255),
                    username VARCHAR(255) UNIQUE,
                    password VARCHAR(255)
                )
            ''')
            conn.commit()
            cursor.close()
            conn.close()
            print("✅ Database initialized successfully")
        except mysql.connector.Error as err:
            print(f"❌ Database Error: {err}")

    def validate_user(self, username, password):
        conn = mysql.connector.connect(database=self.db_name, **self.config)
        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM {self.table_name} WHERE username=%s AND password=%s", (username, password))
        result = cursor.fetchone()
        cursor.close()
        conn.close()
        return result is not None

    def user_exists(self, username):
        conn = mysql.connector.connect(database=self.db_name, **self.config)
        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM {self.table_name} WHERE username=%s", (username,))
        result = cursor.fetchone()
        cursor.close()
        conn.close()
        return result is not None

    def create_user(self, name, username, password):
        conn = mysql.connector.connect(database=self.db_name, **self.config)
        cursor = conn.cursor()
        cursor.execute(f"INSERT INTO {self.table_name} (name, username, password) VALUES (%s, %s, %s)", (name, username, password))
        conn.commit()
        cursor.close()
        conn.close()

    def get_full_name(self, username):
        """
        This method retrieves the full name of a user based on the username.
        """
        conn = mysql.connector.connect(database=self.db_name, **self.config)
        cursor = conn.cursor()
        cursor.execute(f"SELECT name FROM {self.table_name} WHERE username=%s", (username,))
        result = cursor.fetchone()
        cursor.close()
        conn.close()

        if result:
            return result[0]  # Return the full name
        else:
            return None  # Return None if the user is not found