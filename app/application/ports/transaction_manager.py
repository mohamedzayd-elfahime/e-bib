from abc import ABC, abstractmethod


class TransactionManager(ABC):
    """
    Port responsible for database transaction boundaries.
    """

    @abstractmethod
    def begin(self) -> None:
        """
        Start a new transaction.
        """
        raise NotImplementedError

    @abstractmethod
    def commit(self) -> None:
        """
        Commit the current transaction.
        """
        raise NotImplementedError

    @abstractmethod
    def rollback(self) -> None:
        """
        Roll back the current transaction.
        """
        raise NotImplementedError
