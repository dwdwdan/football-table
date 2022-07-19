import sqlite3
from pathlib import Path
import logging
import readline

logging.basicConfig(filename="log.log", encoding="utf-8", level=logging.DEBUG)



def str2bool(string):
    """Converts the given string into a bool. Assumes false unless the answer is affirmative"""
    confirm_choices = ["y", "yes"]
    if string.lower() in confirm_choices:
        return True
    else:
        return False

# This function is stolen from https://eli.thegreenplace.net/2016/basics-of-using-the-readline-library/
def make_completer(vocabulary):
    def custom_complete(text, state):
        # None is returned for the end of the completion session.
        results = [x for x in vocabulary if x.startswith(text)] + [None]
        # A space is added to the completion since the Python readline doesn't
        # do this on its own. When a word is fully completed we want to mimic
        # the default readline library behavior of adding a space after it.
        return results[state] + " "
    return custom_complete

    
def main():
    available_commands = {
        "quit": None,
        "empty database": generate_empty_db,
        "new team": new_team,
        "print teams": print_teams
    }

    # We always want to connect to the database, otherwise this
    # software does nothing useful.
    db_file = Path("database.db")
    connect_to_db(db_file)

    # print("Type \"help\" for help information")
    # main CLI loop
    running = True
    while running:
        readline.parse_and_bind('tab: complete')
        readline.set_completer(make_completer(available_commands))
        wanted_command = input("-> ").strip()
        if wanted_command == "quit":
            logging.info("Quiting application")
            running = False
        elif wanted_command in available_commands:
            available_commands[wanted_command]()
        else:
            print("That is not a valid command. Type \"quit\" to exit the application.")

    conn.close()

def connect_to_db(db_file):
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
    logging.info(f"Connected to database stored at {db_file}")

    if create_tables:
        generate_empty_db()

def generate_empty_db():
    """Creates required tables. WARNING: THIS WILL DELETE ALL DATA"""
    # We want to check with the user that this is what they want us to
    # do, as it is a destructive action, that can be run automatically
    # on startup
    confirmation = input(f"Do you want to generate a new empty database?\n THIS WILL DELETE ALL DATA (enter Y to confirm)")
    if str2bool(confirmation) is True:
        logging.info(f"Recreating database content")
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
            logging.error(f"Recreating content has failed with error message {e}")
            cur.execute("ROLLBACK;")

def new_team(team_name=None):
    """Add a new team into the database"""
    if team_name==None:
        team_name = input("Enter team name\n")

    # first I want to check whether a team of that name already
    # exists. If it does, don't add the team and tell the user.
    cur.execute(f"SELECT * FROM teams WHERE name=\"{team_name}\";")
    if cur.fetchone() is None:
        cur.execute("INSERT INTO teams(name) VALUES (?)", (team_name,))
        logging.info(f"New team {team_name} was created")
    else:
        print("This team already exists")

def get_teams():
    cur.execute("SELECT name FROM teams")
    teams = []
    for team in cur.fetchall():
        teams.append(team[0])
    return teams

def get_team_id(team_name):
    cur.execute(f"SELECT id FROM teams WHERE name=\"{team_name}\"")
    id = cur.fetchone()
    # I need to check that a team with the given name actually exists.
    if id is None:
        print("There is no team with that ID")
        # TODO: give this exceotion a specific type
        raise Exception
    else:
        # id is a tuple of length one, but I want to return the number
        return id[0]

def print_teams():
    """Print a list of teams in the database"""
    print("Teams")
    print("-------")
    for team in get_teams():
        print(team)
