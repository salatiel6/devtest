from .db_inteface import DatabaseInterface


class DatabaseContext:
    def __init__(self, db_instance: DatabaseInterface) -> None:
        """
        Initialize the DatabaseContext.

        :param db_instance: [ElevatorDatabase] An instance of ElevatorDatabase

        :return: [None]
        """
        self.db_instance = db_instance

    def __enter__(self) -> DatabaseInterface:
        """
        Enter the context and establish a database connection.

        :return: [ElevatorDatabase] The ElevatorDatabase instance
        """
        self.db_instance.connect()
        return self.db_instance

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        """
        Exit the context and close the database connection.

        :return: [None]
        """
        self.db_instance.close_connection()
