import re
import json
from .jsondbexceptions import *

class JsondbIo:
    @classmethod
    def validate(cls, name, type):
        if not re.match(r'^[a-zA-Z_]+[0-9]*$', name):
            raise InvalidName(f"Invalid {type} name. It should contain only letters, underscores, and numbers")
    
    @classmethod
    def read(cls, filename, payload):
        try:
            with open(str(filename), 'r', encoding='UTF-8') as file:
                data = json.load(file)
        except FileNotFoundError:
            raise ErrorReadingCollection(cls.msg(ErrType.ErrorReadingCollection, payload))
        return data
    
    @classmethod
    def write(cls, filename, data, payload):
        try:
            with open(str(filename), 'w', encoding='UTF-8') as file:
                json.dump(data, file)
        except FileNotFoundError:
            raise ErrorWritingCollection(cls.msg(ErrType.ErrorWritingCollection, payload))
    
    @classmethod
    def msg(cls, type, payload: dict):
        match type:
            case ErrType.DatabaseAlreadyExist:
                return f"[{payload['operation']}]: Database '{payload['name']}' already exists."
            case ErrType.DatabaseNotFound:
                return f"[{payload['operation']}]: Database '{payload['name']}' not found!"
            case ErrType.CollectionAlreadyExist:
                return f"[{payload['operation']}]: Collection '{payload['name']}' already exists."
            case ErrType.DatabaseNotFound:
                return f"[{payload['operation']}]: Database '{payload['name']}' not found!"
            case ErrType.InvalidDatabasePath:
                return f"[{payload['operation']}]: Path for database [{payload['path']}] is invalid"
            case ErrType.InvalidCollectionPath:
                return f"[{payload['operation']}]: Path for collection [{payload['path']}] is invalid"
            case ErrType.ErrorReadingCollection:
                return f"[{payload['operation']}]: Error parsing collection"
            case ErrType.ErrorWritingCollection:
                return f"[{payload['operation']}]: Error updating collection"
            