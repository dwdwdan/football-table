from football_table import cli as ft
import pytest
from pathlib import Path

test_db_file = Path("database_test.db")

@pytest.mark.parametrize('string, expected', [("y", True), ("Y", True), ("yes", True), ("Yes", True), ("n", False), ("43", False)])
def test_str2bool(string, expected):
    assert(ft.str2bool(string) == expected)

def create_test_db():
    ft.connect_to_db(test_db_file, interactive=False)
    ft.generate_empty_db(interactive=False)
    example_teams = ["Team A", "Team B", "Team C", "Team D"]
    for team in example_teams:
        ft.new_team(team)

def load_test_db():
    ft.connect_to_db(test_db_file, interactive=False)

def test_get_teams():
    create_test_db()
    assert(ft.get_teams() == ["Team A", "Team B", "Team C", "Team D"])

def test_get_team_id_valid_name():
    create_test_db()
    assert(ft.get_team_id("Team A") == 1)

def test_get_team_id_invalid_name():
    create_test_db()
    with pytest.raises(Exception):
        ft.get_team_id("A non-existing team")

def test_new_team():
    create_test_db()
    test_team_name = "Team E"
    ft.new_team(test_team_name)

    # If this runs successfully, we know that it has been created
    # properly.
    ft.get_team_id(test_team_name)

def test_delete_team():
    create_test_db()
    team_to_delete = "Team A"
    ft.delete_team(team_to_delete)

    # If this function raises an exception, we know that the team no
    # longer exists in the db
    with pytest.raises(Exception):
        ft.get_team_id(team_to_delete)

def test_rename_team():
    create_test_db()
    team_to_rename = "Team D"
    rename_to = "Team D test"

    ft.rename_team(team_to_rename, rename_to)

    with pytest.raises(Exception):
        ft.get_team_id(team_to_rename)

    ft.get_team_id(rename_to)
