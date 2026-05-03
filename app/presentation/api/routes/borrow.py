from fastapi import APIRouter, Depends, HTTPException

from app.infrastructure.db.session.mysql import get_connection
from app.infrastructure.db.transaction_manager_mysql import MySQLTransactionManager
from app.infrastructure.repos.book_copy_repository_mysql import BookCopyRepositoryMySQL
from app.infrastructure.repos.borrowing_repository_mysql import BorrowingRepositoryMySQL
from app.infrastructure.time.system_clock import SystemClock

from app.application.use_cases.borrow_book import BorrowBookUseCase
from app.application.dto.borrow_book import BorrowBookCommand
from app.application.policies.borrowing_policy import BorrowingPolicy

from app.presentation.api.dependencies import get_current_user_id


router = APIRouter()


@router.post("/borrow/{isbn}")
def borrow_book(
    isbn: str,
    current_user=Depends(get_current_user_id),
):
    # 1) Open DB connection (infrastructure concern)
    connection = get_connection()

    # 2) Transaction manager
    tx = MySQLTransactionManager(connection)

    # 3) Repositories (shared connection)
    book_copy_repo = BookCopyRepositoryMySQL(connection)
    borrowing_repo = BorrowingRepositoryMySQL(connection)

    # 4) Application policy
    borrowing_policy = BorrowingPolicy(borrowing_repo)

    # 5) Use case
    use_case = BorrowBookUseCase(
        book_copy_repository=book_copy_repo,
        borrowing_repository=borrowing_repo,
        borrowing_policy=borrowing_policy,
        transaction_manager=tx,
        clock=SystemClock(),
    )

    command = BorrowBookCommand(
        user_id=current_user,
        isbn=isbn,
    )

    try:
        result = use_case.execute(command)

        if not result.success:
            raise HTTPException(status_code=400, detail=result.reason)

        return {"status": "ok"}

    finally:
        connection.close()
