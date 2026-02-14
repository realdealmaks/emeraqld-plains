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
    except Exception as e:
        print(f"error loading {json_filename}: {e}")
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

def has_save_in_db(db_filename="game_data.db"):
    if not os.path.exists(db_filename):
        return False

    try:
        conn = sqlite3.connect(db_filename)
        cursor = conn.cursor()

        # check for save things
        cursor.execute("""
            SELECT key, value FROM game_data 
            WHERE key IN ('last_health', 'last_wealth', 'last_inventory', 'last_position', 'last_weapons', 'last_tilemap_calls')
        """)
        rows = cursor.fetchall()
        conn.close()

        if not rows:
            return False

        # check for non default
        for key, value in rows:
            try:
                val = json.loads(value)
                if key == 'last_health' and val > 0:
                    return True
                if key == 'last_wealth' and val > 0:
                    return True
                if key == 'last_inventory' and len(val) > 0:
                    return True
                if key == 'last_position' and val != [0, 0]:
                    return True
            except:
                pass

        return False
    except Exception as e:
        print(f"error {e}")
        return False