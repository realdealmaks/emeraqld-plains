# databes

import sqlite3, json, os

# stores data from json to db when quit

def save_db(json_filename="data.json", db_filename="game_data.db"):
    if not os.path.exists(json_filename):
        print(f"{json_filename} does not exist")
        return

    try:
        with open(json_filename, "r") as f:
            data = json.load(f)
    except json.JSONDecodeError:
        print(f"{json_filename} is not valid JSON. Migration aborted.")
        return

    conn = sqlite3.connect(db_filename)
    cursor = conn.cursor()

    # if doesnt exist
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS game_data (
            key TEXT PRIMARY KEY,
            value TEXT
        )
    """)

    cursor.execute("SELECT * FROM game_data")
    rows = cursor.fetchall()
    print("db contents:")
    for row in rows:
        print(row)
    conn.commit()

    conn.close()
