from src import Database
from pathlib import Path
import json

database = Database('customers')
path = Path('customers/credentials.json')

def test_create_document():
    database.create()
    database.add('credentials')
    collection = database.collection('credentials')
    documents = [
        {
            "username": "bit-web24",
            "email": "example@gmail.com",
            "password": "p4ssw0r6",
        },
        {
            "username": "name34",
            "email": "example345@example.com",
            "password": "password",
        }
    ]
    collection.add(documents)
    with open(str(path), 'r') as file:
        data = json.load(file)
    assert data == documents

def test_get_document():
    collection = database.collection('credentials')
    docs = collection.get(lambda document: document['username'] == "bit-web24")
    assert docs == [{
        "username": "bit-web24",
        "email": "example@gmail.com",
        "password": "p4ssw0r6",
    }]

def test_update_document():
    collection = database.collection('credentials')
    def update(document):
        if document['username'] == 'bit-web24':
            document['email'] = "example3021@gmail.com"
    collection.set(update)
    docs = collection.get(lambda document: document['username'] == "bit-web24")
    assert docs == [{
        "username": "bit-web24",
        "email": "example3021@gmail.com",
        "password": "p4ssw0r6",
    }]

def test_remove_document():
    collection = database.collection('credentials')
    collection.remove(lambda document: document['username'] == 'name34')
    docs = collection.get(lambda document: document['username'] == "name34")
    assert docs == []

def test_delete_collection():
    collection = database.collection('credentials')
    collection.delete()
    assert path.exists() == False

def test_delete_database():
    database.delete()
    assert path.parent.exists() == False
