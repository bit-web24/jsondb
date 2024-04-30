from src import Database
from pathlib import Path

database = Database('users')

def test_create_database():
    database.create()
    p = Path('users')
    assert p.exists() == True

def test_rename_database():
    database.rename('credentials')
    old_path = Path('users')
    new_path = Path('credentials')
    assert old_path.exists() == False
    assert new_path.exists() == True

def test_delete_database():
    database.delete()
    p = Path('credentials')
    assert p.exists() == False
