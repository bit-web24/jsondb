from src import Database
from pathlib import Path

database = Database('customers')
path = Path('customers/credentials.json')

def test_create_collection():
    database.create()
    database.add('credentials')
    assert path.exists() == True

def test_get_collection():
    assert path.exists() == True

def test_rename_collection():
    collection = database.collection('credentials')
    collection.rename('usernameandpassword')
    assert path.exists() == False
    tmp_path = Path('customers/usernameandpassword.json')
    assert tmp_path.exists() == True
    
def test_delete_collection():
    collection = database.collection('usernameandpassword')
    collection.delete()
    assert path.exists() == False

def test_delete_database():
    database.delete()
    p = Path('customers')
    assert p.exists() == False
