import sqlite3


def execute_query(sql_query):
    with sqlite3.connect('login.db') as conn:
        cur = conn.cursor()
        result = cur.execute(sql_query)
        conn.commit()
    return result


def insert_user(email, password):
    sql_query = "INSERT INTO users(email, password) VALUES('%s', '%s')" % (email, password)
    execute_query(sql_query)

def get_password(email):
    sql_query = "SELECT password FROM users WHERE email='%s' " % (email)
    password = execute_query(sql_query).fetchall()
    return password


if __name__ == '__main__':
    get_password('20ao40@kcgcollege.com')