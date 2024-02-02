from abc import ABC, abstractmethod


class DatabaseInterface(ABC):
    @abstractmethod
    def connect(self) -> None:
        """Connect to the database"""
        pass

    @abstractmethod
    def close_connection(self) -> None:
        """Close connection with the database"""
        pass
