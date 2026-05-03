from app.application.ports.book_repository import BookReadRepository
from app.application.ports.favorite_repository import FavoriteRepository
from app.application.filters.book_filters import BookFilters
from app.application.read_models.pagination import PaginatedResult
from app.application.read_models.book import BookListItem
from app.application.ports.category_repository import CategoryRepositoryMySQL    
class ListBooksUseCase:
    """
    Use case for listing books (all books page).

    Responsibilities:
    - retrieve paginated books using read repository
    - retrieve user favorites
    - enrich BookListItem.is_favorite
    """

    def __init__(
        self,
        book_repo: BookReadRepository,
        favorite_repo: FavoriteRepository,
            category_repo: CategoryRepositoryMySQL, 
    ):
        self.book_repo = book_repo
        self.favorite_repo = favorite_repo
        self.category_repo = category_repo

    def execute(
        self,
        *,
        filters: BookFilters,
        page: int,
        size: int,
        user_id: int,
    ) -> PaginatedResult[BookListItem]:
        categories = self.category_repo.list_with_book_count()


        
        result =  self.book_repo.list_books(
            user_id=user_id,
            filters=filters,
            page=page,
            size=size,
        )

        favorite_isbns =  self.favorite_repo.get_favorite_isbns(
            user_id=user_id
        )
        favorite_set = set(favorite_isbns)

        for item in result.items:
            item.is_favorite = item.isbn in favorite_set

        return result , categories
