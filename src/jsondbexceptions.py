from enum import Enum

class CustomDatabaseException(Exception):
    """Base class for custom database exceptions."""
    def __init__(self, message: str) -> None:
        super().__init__(message)


class CollectionNotFound(CustomDatabaseException):
    """Exception raised when a collection is not found."""
    pass


class DatabaseNotFound(CustomDatabaseException):
    """Exception raised when a database is not found."""
    pass


class DocumentNotFound(CustomDatabaseException):
    """Exception raised when a document is not found."""
    pass


class DatabaseAlreadyExist(CustomDatabaseException):
    """Exception raised when trying to create a database that already exists."""
    pass


class CollectionAlreadyExist(CustomDatabaseException):
    """Exception raised when trying to create a collection that already exists."""
    pass


class CannotRenameDatabase(CustomDatabaseException):
    """Exception raised when renaming a database is not possible."""
    pass


class InvalidDatabasePath(CustomDatabaseException):
    """Exception raised when an invalid database path is provided."""
    pass


class InvalidCollectionPath(CustomDatabaseException):
    """Exception raised when an invalid database path is provided."""
    pass


class ErrorReadingCollection(CustomDatabaseException):
    """Exception raised when trying to read from a collection"""
    pass


class ErrorWritingCollection(CustomDatabaseException):
    """Exception raised when trying to write to a collection"""
    pass

class InvalidName(CustomDatabaseException):
    """Exception raised when given invalid name for collection/database"""
    pass

class ErrType(Enum):
    CollectionNotFound = 1
    DatabaseNotFound = 2
    DocumentNotFound = 3
    DatabaseAlreadyExist = 4
    CollectionAlreadyExist = 5
    CannotRenameDatabase = 6
    InvalidDatabasePath = 7
    InvalidCollectionPath = 8
    ErrorReadingCollection = 9
    ErrorWritingCollection = 10
    InvalidName = 11
    