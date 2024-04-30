import copy
from pathlib import Path
from .jsondbio import JsondbIo
from .jsondbexceptions import *

class Database:
    def __init__(self, database_path: str) -> None:
        self.database = Path(database_path).resolve()

    def create(self):
        if self.database.exists():
            raise DatabaseAlreadyExist(JsondbIo.msg(ErrType.DatabaseAlreadyExist, {
                'name': self.database.name,
                'operation': 'CREATE_DATABASE'
            }))
        
        try:
            self.database.mkdir()
        except FileNotFoundError:
            raise InvalidDatabasePath(JsondbIo.msg(ErrType.InvalidDatabasePath, {
                'path': str(self.database),
                'operation': 'CREATE_DATABASE'
            }))


    def collection(self, collection_name: str):
        JsondbIo.validate(collection_name, 'collection')
        collection_path = self.database.joinpath(collection_name + '.json')
        if collection_path.exists():
            return _Collection(collection_path)
        raise CollectionNotFound(JsondbIo.msg(CollectionNotFound, {
            'name': collection_path.name[:-6],
            'operation': 'GET_COLLECTION'
        }))


    def add(self, collection_name: str):
        JsondbIo.validate(collection_name, 'collection')
        if not self.database.exists():
            raise DatabaseNotFound(JsondbIo.msg(ErrType.DatabaseNotFound, {
                'name': self.database.name,
                'operation': 'CREATE_COLLECTION'
            }))
        
        collection_path = self.database.joinpath(collection_name + '.json')
        if collection_path.exists():
            raise CollectionAlreadyExist(JsondbIo.msg(ErrType.CollectionAlreadyExist, {
                'name': collection_name,
                'operation': 'CREATE_COLLECTION'
            }))
        
        collection_path.touch()
        collection_path.write_text('[]')


    def rename(self, new_database_name: str):
        JsondbIo.validate(new_database_name, 'database')
        if not self.database.exists():
            raise DatabaseNotFound(JsondbIo.msg(ErrType.DatabaseNotFound, {
                'name': self.database.name,
                'operation': 'RENAME_DATABASE'
            }))
        
        new_database_path = self.database.parent.joinpath(new_database_name)
        if new_database_path.exists():
            raise DatabaseAlreadyExist(JsondbIo.msg(ErrType.DatabaseAlreadyExist, {
                'name': new_database_path.name,
                'operation': 'RENAME_DATABASE'
            }))
        
        self.database = self.database.rename(new_database_path)


    def delete(self):
        if not self.database.exists():
            raise DatabaseNotFound(JsondbIo.msg(ErrType.DatabaseNotFound, {
                'name': self.database.name,
                'operation': 'DELETE_DATABASE'
            }))
        def delete_folder_contents(folder):
            for item in folder.iterdir():
                if item.is_file():
                    item.unlink()
                elif item.is_dir():
                    delete_folder_contents(item)
                    item.rmdir()
        delete_folder_contents(self.database)
        self.database.rmdir()


class _Collection:
    def __init__(self, collection_path: str) -> None:
        self.collection_path = collection_path


    def add(self, document):
        data = JsondbIo.read(self.collection_path, {
            'operation': 'ADD_DOCUMENT'
        })
        if isinstance(document, dict):
            data.append(document)
        elif isinstance(document, list):
            data.extend(list(filter(lambda datum: isinstance(datum, dict), document)))
        JsondbIo.write(self.collection_path, data, {
            'operation': 'ADD_DOCUMENT'
        })


    def get(self, func):
        json_data = JsondbIo.read(self.collection_path, {
            'operation': 'GET_DOCUMENT'
        })
        return [document for document in json_data if func(_Document(document)) == True]


    def remove(self, func):
        json_data = JsondbIo.read(self.collection_path, {
            'operation': 'REMOVE_DOCUMENT'
        })
        data = [document for document in json_data if func(_Document(document)) == False]
        JsondbIo.write(self.collection_path, data, {
            'operation': 'REMOVE_DOCUMENT'
        })


    def set(self, func):
        json_data = JsondbIo.read(self.collection_path, {
            'operation': 'UPDATE_DOCUMENT'
        })
        data = []
        for document in json_data:
            doc = _Document(document, writable=True)
            func(doc)
            data.append(doc.parse())
        JsondbIo.write(self.collection_path, data, {
            'operation': 'UPDATE_DOCUMENT'
        })


    def rename(self, new_collection_name: str):
        new_path = self.collection_path.parent.joinpath(new_collection_name + '.json')
        try:
            self.collection_path = self.collection_path.rename(str(new_path))
        except FileNotFoundError:
            raise InvalidCollectionPath(JsondbIo.msg(ErrType.InvalidCollectionPath, {
                'name': new_path.name[:-6],
                'operation': 'RENAME_COLLECTION'
            }))
        

    def delete(self):
        try:
            self.collection_path.unlink()
        except FileNotFoundError:
            raise CollectionNotFound(JsondbIo.msg(ErrType.CollectionNotFound, {
                'name': self.collection_path.name[:-6],
                'operation': 'DELETE_COLLECTION'
            }))


class _Document:
    def __init__(self, document: dict, writable=False):
        self.writable = writable
        self.document = document
    
    def __getitem__(self, key):
        return self.document.get(key)

    def __setitem__(self, key, value):
        if self.writable:
            self.document[key] = value

    def remove(self, key):
        if self.writable and self.document.get(key):
            self.document.pop(key)
        
    def parse(self):
        return copy.deepcopy(self.document)
    
