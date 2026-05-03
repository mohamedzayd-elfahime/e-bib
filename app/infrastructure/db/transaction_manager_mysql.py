# app/infrastructure/db/transaction_manager_mysql.py

from app.application.ports.transaction_manager import TransactionManager


class MySQLTransactionManager(TransactionManager):
    def __init__(self, connection):
        self.connection = connection

    def begin(self) -> None:
        # start transaction
        self.connection.autocommit = False

    def commit(self) -> None:
        # validate transaction
        self.connection.commit()
        self.connection.autocommit = True

    def rollback(self) -> None:
        # cancel transaction
        self.connection.rollback()
        self.connection.autocommit = True
