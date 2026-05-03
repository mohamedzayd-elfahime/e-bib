from fastapi import APIRouter, Depends, HTTPException
from starlette import status
from app.infrastructure.db.session.mysql import get_connection
from app.infrastructure.db.transaction_manager_mysql import MySQLTransactionManager
from app.infrastructure.repos.reservation_repository_mysql import ReservationRepositoryMySQL
from app.infrastructure.repos.book_copy_repository_mysql import BookCopyRepositoryMySQL

from app.application.use_cases.reserve_book import ReserveBookUseCase
from app.application.policies.reservation_policy import ReservationPolicy
from app.application.dto.reserve_book import ReserveBookCommand

from app.presentation.api.dependencies import get_current_user_id
from app.application.use_cases.cancel_reservation import CancelReservationUseCase


router = APIRouter()


@router.post("/books/{isbn}/reserve")
def reserve_book(
    isbn: str,
    current_user=Depends(get_current_user_id),
):
    conn = get_connection()
    tx = MySQLTransactionManager(conn)

    reservation_repo = ReservationRepositoryMySQL(conn)
    book_copy_repo = BookCopyRepositoryMySQL(conn)

    policy = ReservationPolicy(
        reservation_repository=reservation_repo,
        book_copy_repository=book_copy_repo,
    )

    use_case = ReserveBookUseCase(
        reservation_repository=reservation_repo,
        reservation_policy=policy,
        transaction_manager=tx,
    )

    command = ReserveBookCommand(
        user_id=current_user,
        isbn=isbn,
    )

    try:
        result = use_case.execute(command)

        if not result.success:
            raise HTTPException(status_code=400, detail=result.reason)

        return {"status": "ok"}

    finally:
        conn.close()

@router.post("/books/{isbn}/reserve/cancel")
def cancel_reservation(
    isbn: str,
    current_user=Depends(get_current_user_id),
):
    conn = get_connection()

    try:
        reservation_repo = ReservationRepositoryMySQL(conn)

        use_case = CancelReservationUseCase(
            reservation_repository=reservation_repo,
        )

        use_case.execute(
            user_id=current_user,
            isbn=isbn,
        )

        return {"status": "cancelled"}

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )

    finally:
        conn.close()
