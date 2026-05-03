from fastapi import APIRouter, Request , Depends , Query
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi import APIRouter, Request, Form, HTTPException, status
from fastapi.responses import RedirectResponse
from pydantic import EmailStr
from app.application.use_cases.login_user import LoginUser, InvalidCredentials
from app.infrastructure.repos.user_repository_mysql import MySQLUserRepository
from app.infrastructure.security.password_hasher import Argon2PasswordHasher
from app.infrastructure.security.jwt_service import JwtTokenService
from app.infrastructure.repos.book_repository_mysql import BookRepositoryMySQL
from app.infrastructure.repos.book_copy_repository_mysql import BookCopyRepositoryMySQL
from app.application.use_cases.get_home_books import GetHomeBooksUseCase
from app.presentation.api.dependencies import get_current_user_id
from app.infrastructure.repos.favorite_repository_mysql import MySQLFavoriteRepository
from app.infrastructure.repos.category_repository_mysql import CategoryRepositoryMySQL
from app.application.use_cases.list_books import ListBooksUseCase
from app.application.filters.book_filters import BookFilters
from app.application.use_cases.get_book_detail import GetBookDetail
from app.infrastructure.db.session.mysql import get_connection
from app.infrastructure.repos.borrowing_repository_mysql import BorrowingRepositoryMySQL
from app.infrastructure.repos.reservation_repository_mysql import ReservationRepositoryMySQL
from app.application.use_cases.get_suggested_books import GetSuggestedBooksUseCase

# Router SSR pages
router = APIRouter()

# Jinja templates directory
templates = Jinja2Templates(
    directory="app/presentation/templates"
)


@router.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse(
        "home_user.html",
        {"request": request}
    )

@router.get("/home", response_class=HTMLResponse)
async def home(request: Request,
               user_id: int = Depends(get_current_user_id),):
    book_repo = BookRepositoryMySQL()
    favorite_repo = MySQLFavoriteRepository()
    use_case = GetHomeBooksUseCase(book_repo,favorite_repo)

    latest_books = await use_case.execute(limit_per_category=5, user_id=user_id)

    return templates.TemplateResponse(
        "home_user.html",
        {
            "request": request,
            "latest_books": latest_books,
            "csrf_token": request.session.get("csrf_token"),
        }
    )



@router.get("/books", response_class=HTMLResponse)
async def get_books(
    request: Request,
    page: int = Query(1, ge=1),
    category: str | None = None,
    author: str | None = None,
    search: str | None = None,
    current_user=Depends(get_current_user_id),
):
    filters = BookFilters(
        category=category,
        author=author,
        search=search,
    )

    uc = ListBooksUseCase(
        book_repo=BookRepositoryMySQL(),
        favorite_repo=MySQLFavoriteRepository(),
        category_repo=CategoryRepositoryMySQL(),
    )

    result, categories = uc.execute(
        filters=filters,
        page=page,
        size=6,
        user_id=current_user,
    )

    context = {
        "request": request,
        "books": result.items,
        "page": result.page,
        "total": result.total,
        "size": result.size,
        "filters": filters,
        "categories": categories,
    }

    if request.headers.get("X-Requested-With") == "XMLHttpRequest":
        print("AJAX request - returning partial HTML")
        return templates.TemplateResponse(
            "books_user.html",{
            **context,
            "csrf_token": request.session.get("csrf_token"),}
        )

    return templates.TemplateResponse(
            "books_user.html",{
            **context,
            "csrf_token": request.session.get("csrf_token"),}
        )


@router.get("/login")
async def login(request: Request):
    return templates.TemplateResponse(
        "login.html",
        {
            "request": request,
            "csrf_token": request.session.get("csrf_token"),
        }
    )



@router.get("/register", response_class=HTMLResponse)
async def register(request: Request):
    return templates.TemplateResponse(
        "register.html",
        {"request": request}
    )

@router.get("/books_details", response_class=HTMLResponse)
async def register(request: Request):
    return templates.TemplateResponse(
        "book_details_user.html",
        {"request": request}
    )

@router.get("/books/{isbn}", response_class=HTMLResponse)
async def get_book_detail(
    request: Request,
    isbn: str,
    current_user=Depends(get_current_user_id),
):
    conn = get_connection()

    # --- Use case : Book detail ---
    book_uc = GetBookDetail(
        book_repo=BookRepositoryMySQL(),
        book_copy_repo=BookCopyRepositoryMySQL(conn),
        favorite_repo=MySQLFavoriteRepository(),
        borrowing_repo=BorrowingRepositoryMySQL(conn),
        reservation_repo=ReservationRepositoryMySQL(conn),
    )

    book = book_uc.execute(
        isbn=isbn,
        user_id=current_user,
    )

    # --- Use case : Suggested books ---
    suggested_uc = GetSuggestedBooksUseCase(
        book_repo=BookRepositoryMySQL(),
        book_copy_repo=BookCopyRepositoryMySQL(conn),
        favorite_repo=MySQLFavoriteRepository(),
    )

    suggested_books = suggested_uc.execute(
        isbn=isbn,
        user_id=current_user,
        limit=3,
    )

    context = {
        "request": request,
        "book": book,
        "suggested_books": suggested_books,
        "csrf_token": request.session.get("csrf_token"),
    }

    return templates.TemplateResponse(
        "book_details_user.html",
        context,
    )
