from utils.handle_time import calculate_elapsed
import sqlite3

conn = None
COLUMNS = "USER_NM, STD_AMT, STD_CNT, LAST_LOGIN_HMS, LAST_OUT_HMS"

def init_db(db_name, table_name):
    global conn
    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    c.execute(f"SELECT COUNT(*) FROM sqlite_master WHERE name='{table_name}';")

    if c.fetchone()[0] == 0:
        c.execute(f"CREATE TABLE {table_name}(USER_NM text, STD_AMT int, STD_CNT int, LAST_LOGIN_HMS timestamp, LAST_OUT_HMS timestamp);")
    conn.commit()

def start_study(user_name, table_name, current_time):
    global conn
    print(f"start study : {current_time}")
    query = None
    datas = None

    c = conn.cursor()
    c.execute(f"SELECT * FROM {table_name} WHERE USER_NM = ?", (user_name, ))
    rows = c.fetchall()
    if len(rows) == 0:
        query = f"INSERT INTO {table_name}({COLUMNS}) VALUES (?, ?, ?, ?, ?)"
        datas = [user_name, 0, 0, current_time, "NULL"]
        print(f"New User : {user_name}")
    else:
        c.execute(f"SELECT * FROM {table_name} WHERE USER_NM = ?", (user_name, ))
        query = f"UPDATE {table_name} SET LAST_LOGIN_HMS = ? WHERE USER_NM = ?"
        datas = [current_time, user_name]

    c.execute(query, datas)
    conn.commit()

    return None

def end_study(user_name, table_name, current_time):
    global conn
    print(f"end study : {current_time}")
    query = f"UPDATE {table_name} SET STD_AMT = ?,  STD_CNT = ?, LAST_LOGIN_HMS =?, LAST_OUT_HMS = ? WHERE USER_NM = ?"
    datas = []

    c = conn.cursor()
    c.execute(f"SELECT * FROM {table_name} WHERE USER_NM=?", (user_name,))
    rows = c.fetchall()[0]
    
    if len(rows) == 0:
        print(f"New User : {user_name}")
        return -1
    
    start_time = rows[3]
    elapsed_time = calculate_elapsed(start_time, current_time).total_seconds()
    datas = (rows[1]+elapsed_time, rows[2]+1, "NULL", current_time, user_name)

    c.execute(query, datas)
    conn.commit()

    return None

def list_study(table_name):
    global conn
    c = conn.cursor()
    c.execute(f"SELECT * FROM {table_name}")
    rows = c.fetchall()
    conn.commit()
    results = ""
    for row in rows:
        results += str(row) + "\n"
    return results

def close_db():
    global conn
    conn.close()

    return None

def edit_time(user_name, edit_type):
    return None