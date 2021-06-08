from utils.handle_time import calculate_elapsed
import sqlite3
from dotenv import load_dotenv

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
    try:
        c.execute(f"SELECT * FROM {table_name} WHERE USER_NM == {user_name}")
        query = f"UPDATE {table_name} SET LAST_LOGIN_HMS = ? WHERE USER_NM = ?"
        datas = [current_time, user_name]
    except sqlite3.OperationalError:
        query = f"INSERT INTO {table_name}({COLUMNS}) VALUES (?, ?, ?, ?, ?)"
        datas = [user_name, 0, 0, "NULL", "NULL"]
        print(f"New User : {user_name}")

    c.execute(query, datas)
    conn.commit()

    return None

def end_study(user_name, table_name, current_time):
    global conn
    print(f"end study : {current_time}")
    query = f"UPDATE INTO {table_name} SET STD_AMT = ?,  STD_CNT = ?, LAST_OUT_HMS = ?, WHERE USER_NM = ?"
    datas = []

    c = conn.cursor()
    try:
        c.execute(f"SELECT * FROM {table_name} WHERE USER_NM == {user_name}")
        rows = c.fetchall()
        start_time = rows[3]
        elapsed_time = calculate_elapsed(start_time, current_time)
        datas = [rows[1]+elapsed_time, rows[2]+1, current_time, user_name]
    except sqlite3.OperationalError:
        print(f"New User : {user_name}")
        return -1

    c.execute(query, datas)
    conn.commit()

    return None

def list_study(table_name):
    global conn    
    c = conn.cursor()
    c.execute(f"SELECT * FROM {table_name}")
    rows = c.fetchall()
    conn.commit()

    return rows

def edit_time(user_name, edit_type):
    return None