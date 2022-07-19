from football_table import cli as ft
import pytest

@pytest.mark.parametrize('string, expected', [("y", True), ("Y", True), ("yes", True), ("Yes", True), ("n", False), ("43", False)])
def test_str2bool(string, expected):
    assert(ft.str2bool(string) == expected)
