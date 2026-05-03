from fastapi import APIRouter, Depends, HTTPException

from app.infrastructure.db.session.mysql import get_connection
from app.infrastructure.db.transaction_manager_mysql import MySQLTransactionManager
from app.infrastructure.repos.borrowing_repository_mysql import BorrowingRepositoryMySQL
from app.infrastructure.repos.book_copy_repository_mysql import BookCopyRepositoryMySQL

from app.application.use_cases.return_book import ReturnBookUseCase
from app.presentation.api.dependencies import get_current_user_id
from app.infrastructure.event_bus.bus import event_bus



router = APIRouter()


@router.post("/borrowings/{borrowing_id}/return")
def return_book(
    borrowing_id: int,
    current_user=Depends(get_current_user_id),
):
    connection = get_connection()

    tx = MySQLTransactionManager(connection)

    borrowing_repo = BorrowingRepositoryMySQL(connection)
    book_copy_repo = BookCopyRepositoryMySQL(connection)

    use_case = ReturnBookUseCase(
        borrowing_repository=borrowing_repo,
        book_copy_repository=book_copy_repo,
        transaction_manager=tx,
        event_bus=event_bus,
    )

    try:
        result = use_case.execute(borrowing_id)

        if not result.success:
            raise HTTPException(status_code=400, detail=result.reason)

        return {"status": "ok"}

    finally:
        connection.close()

