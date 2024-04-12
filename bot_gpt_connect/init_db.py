import psycopg2

def init_connection():
    conn = psycopg2.connect(dbname="postgres", user="postgres", password="qwerty", host="localhost")
    conn.autocommit = True

    cursor = conn.cursor()
    cursor.execute("BEGIN")
    cursor.execute("SELECT datname FROM pg_database WHERE datname = 'hackaton'")
    exists = cursor.fetchone()

    if not exists:
        cursor.execute("CREATE DATABASE hackaton")

    cursor.close()
    conn.close()

    conn = psycopg2.connect(dbname="hackaton", user="postgres", password="qwerty", host="localhost")
    cursor = conn.cursor()

    sql_file = './init.sql'
    with open(sql_file, 'r') as file:
        sql_script = file.read()

    cursor.execute(sql_script)
    conn.commit()
    cursor.execute("COMMIT")
    return cursor, conn

# if __name__ == "__main__":
#     init_connection()