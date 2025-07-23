import pandas as pd
import sqlite3

connection = None  # global DB connection

def init_db(df):
    global connection
    connection = sqlite3.connect('mydatabase.db', check_same_thread=False)
    df.to_sql('mytable', connection, if_exists='replace', index=False)

def sql_query(query: str):
    return pd.read_sql_query(query, connection).to_dict(orient='records')
