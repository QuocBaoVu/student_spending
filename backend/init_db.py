from db import get_db_connection
from sqlalchemy import text

def execute_sql_script(engine, sql_file):
    try:
        # Read SQL file
        with open(sql_file, 'r') as file:
            sql_commands = file.read()

        # Execute each SQL command
        with engine.connect() as connection:
            for command in sql_commands.split(';'):
                command = command.strip()
                if command:
                    connection.execute(text(command))  # Use text() for raw SQL
            print("Tables created successfully!")
    except Exception as e:
        print(f" Error creating tables: {e}")

def main():
    engine = get_db_connection()
    if engine:
        execute_sql_script(engine, 'create_tables.sql')
        print("SQLite connection closed.")

if __name__ == "__main__":

    main()
