try:
    import sqlite3, json, os
except ImportError as e:
    print(f"missing module {e}")

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

    for key, value in data.items():
        # convert tuple to str
        if isinstance(value, tuple):
            value = ",".join(map(str, value))
        cursor.execute("""
            INSERT INTO game_data (key, value)
            VALUES (?, ?)
            ON CONFLICT(key) DO UPDATE SET value=excluded.value
        """, (key, str(value)))

    cursor.execute("SELECT * FROM game_data")
    rows = cursor.fetchall()
    print("db contents:")
    for row in rows:
        print(row)

    conn.close()
