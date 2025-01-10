from db import get_db_connection

def execute_sql_script(connection, sql_file):
    cursor = connection.cursor()
    try: 
        with open('create_tables.sql', 'r') as file:
            sql_commands = file.read().split(';')

            for command in sql_commands:
                if command.strip():
                    cursor.execute(command)
            connection.commit()
            print('Tables created successfully')
    except Exception as e:
        print(f"Error creating tables: {e}")
    finally:
        cursor.close()

def main():
    connection = get_db_connection()
    if connection:
        execute_sql_script(connection, 'create_tables.sql')
        connection.close()
        print('Close mySQL')

if __name__ == '__main__':
    main()
