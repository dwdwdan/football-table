from football_table import cli as ft
import pytest
from pathlib import Path

@pytest.mark.parametrize('string, expected', [("y", True), ("Y", True), ("yes", True), ("Yes", True), ("n", False), ("43", False)])
def test_str2bool(string, expected):
    assert(ft.str2bool(string) == expected)

def create_test_db():
    test_db_file = Path("database_test.db")
    ft.connect_to_db(test_db_file)
    ft.generate_empty_db(ask_for_confirmation=False)
    example_teams = ["Team A", "Team B", "Team C", "Team D"]
    for team in example_teams:
        ft.new_team(team)

def load_test_db():
    test_db_file = Path("../database_test.db")
    ft.connect_to_db(test_db_file)

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

