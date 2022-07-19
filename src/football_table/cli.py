import sqlite3
from pathlib import Path

db_file = Path("database_test.db")

def str2bool(string):
    """Converts the given string into a bool"""
    confirm_choices = ["y", "yes"]
    if string.lower() in confirm_choices:
        return True
    else:
        return False

    
def main():
    connect_to_db()
    conn.close()

def connect_to_db():
    create_tables = False
    if not db_file.is_file():
        create_tables=True
    # conn and cur are set as globals so they can easily be used in
    # other functions.
    global conn
    global cur
    conn = sqlite3.connect(db_file, isolation_level=None)
    cur = conn.cursor()
    print("Connected to database")

    if create_tables:
        generate_empty_db()

def generate_empty_db():
    """Creates required tables. WARNING: THIS WILL DELETE ALL DATA"""
    confirmation = input(f"Do you want to generate a new empty database?\n THIS WILL DELETE ALL DATA (enter Y to confirm)")
    if str2bool(confirmation) is True:
        try:
            cur.execute("BEGIN TRANSACTION;")
            cur.execute("DROP TABLE IF EXISTS games;")
            cur.execute("DROP TABLE IF EXISTS teams;")
            cur.execute("""CREATE TABLE games (
                "id"	INTEGER NOT NULL UNIQUE,
                "home_team"	INTEGER NOT NULL,
                "away_team"	INTEGER NOT NULL,
                "home_score"	INTEGER,
                "away_score"	INTEGER,
                PRIMARY KEY("id" AUTOINCREMENT))""")
            cur.execute("""CREATE TABLE teams (
                "id"	INTEGER NOT NULL UNIQUE,
                "name"      TEXT,
                PRIMARY KEY("id" AUTOINCREMENT))""")
            cur.execute("COMMIT;")
        except Exception as e:
            print("ERROR: ", e)
            cur.execute("ROLLBACK;")
