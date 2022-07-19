import sqlite3
from pathlib import Path

db_file = Path("database_test.db")

def str2bool(string):
    """Converts the given string into a bool. Assumes false unless the answer is affirmative"""
    confirm_choices = ["y", "yes"]
    if string.lower() in confirm_choices:
        return True
    else:
        return False

    
def main():
    # We always want to connect to the database, otherwise this
    # software does nothing useful.
    connect_to_db()

    # print("Type \"help\" for help information")
    # main CLI loop
    running = True
    while running:
        command = input("-> ")
        match command:
            case "quit":
                running = False
            case "new team":
                new_team()
            case "print teams":
                print_teams()

    conn.close()

def connect_to_db():
    """Connect to the database stored in db_file. If the file does not exist, create it, and populate it with an empty database."""
    create_tables = False
    if not db_file.is_file():
        create_tables=True
    # conn and cur are set as globals so they can easily be used in
    # other functions.
    global conn
    global cur
    # isolation_level=None disables implicit transactions, meaning I
    # have to handle them myself. For me, this is easier to program.
    conn = sqlite3.connect(db_file, isolation_level=None)
    cur = conn.cursor()
    print("Connected to database")

    if create_tables:
        generate_empty_db()

def generate_empty_db():
    """Creates required tables. WARNING: THIS WILL DELETE ALL DATA"""
    # We want to check with the user that this is what they want us to
    # do, as it is a destructive action, that can be run automatically
    # on startup
    confirmation = input(f"Do you want to generate a new empty database?\n THIS WILL DELETE ALL DATA (enter Y to confirm)")
    if str2bool(confirmation) is True:
        try:
            cur.execute("BEGIN TRANSACTION;")
            # first drop the games and teams tables so they can be recreated
            cur.execute("DROP TABLE IF EXISTS games;")
            cur.execute("DROP TABLE IF EXISTS teams;")

            # recreate the games and teams tables
            cur.execute("""CREATE TABLE games (
                "id"	INTEGER NOT NULL UNIQUE,
                "home_team"	INTEGER NOT NULL,
                "away_team"	INTEGER NOT NULL,
                "home_score"	INTEGER,
                "away_score"	INTEGER,
                PRIMARY KEY("id" AUTOINCREMENT))""")
            cur.execute("""CREATE TABLE teams (
                "id"	INTEGER NOT NULL UNIQUE,
                "name"      TEXT NOT NULL UNIQUE,
                PRIMARY KEY("id" AUTOINCREMENT))""")
            cur.execute("COMMIT;")
        except Exception as e:
            print("ERROR: ", e)
            cur.execute("ROLLBACK;")

def new_team():
    """Add a new team into the database"""
    team_name = input("Enter team name\n")

    # first I want to check whether a team of that name already
    # exists. If it does, don't add the team and tell the user.
    cur.execute(f"SELECT * FROM teams WHERE name=\"{team_name}\";")
    if cur.fetchone() is None:
        cur.execute("INSERT INTO teams(name) VALUES (?)", (team_name,))
    else:
        print("This team already exists")

def print_teams():
    """Print a list of teams in the database"""
    cur.execute("SELECT name FROM teams")
    for team in cur.fetchall():
        print(team[0])
