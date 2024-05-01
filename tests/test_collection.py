from src import Database
from pathlib import Path

database = Database('customers')

def test_create_collection():
    database.create()
    database.add('credentials')
    path = Path('customers/credentials.json')
    assert path.exists() == True

def test_get_collection():
    path = Path('customers/credentials.json')
    assert path.exists() == True
    
def test_delete_collection():
    collection = database.collection('credentials')
    collection.delete()
    path = Path('customers/credentials.json')
    assert path.exists() == False

def test_delete_database():
    database.delete()
    p = Path('credentials')
    assert p.exists() == False
