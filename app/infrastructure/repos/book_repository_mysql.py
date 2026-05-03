from collections import defaultdict
from app.infrastructure.db.session.mysql import get_connection

from app.application.ports.book_repository import BookReadRepository
from app.application.read_models.book import BookListItem, BookDetail
from app.application.read_models.pagination import PaginatedResult
from app.application.filters.book_filters import BookFilters


class BookRepositoryMySQL(BookReadRepository):

    # ---------- HOME PAGE ----------
    def _compute_status(self, row) -> str:
        if row["user_active_borrow_count"] > 0:
            return "borrowed"

        if row["user_active_reservation_count"] > 0:
            return "reserved"

        if row["available_copies"] == 0:
            return "not_available"

        return "available"

    
    async def get_latest_books_by_category(
    self,
    *,
    limit_per_category: int
) -> dict[str, list[BookListItem]]:

        query = """
            SELECT isbn, title, author, cover_url, category
            FROM (
                SELECT
                    b.isbn,
                    b.title,
                    b.author,
                    b.cover_url,
                    c.name AS category,
                    ROW_NUMBER() OVER (
                        PARTITION BY c.id
                        ORDER BY b.isbn DESC
                    ) AS rn
                FROM books b
                JOIN categories c ON c.id = b.category_id
            ) t
            WHERE rn <= %s
            ORDER BY category, isbn DESC
        """

        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute(query, (limit_per_category,))
        rows = cursor.fetchall()

        cursor.close()
        conn.close()

        grouped: dict[str, list[BookListItem]] = defaultdict(list)

        for row in rows:
            grouped[row["category"]].append(
                BookListItem(
                    isbn=row["isbn"],
                    title=row["title"],
                    author=row["author"],
                    category=row["category"],
                    cover_url=row["cover_url"],
                )
            )

        return grouped


    # ---------- ALL BOOKS PAGE ----------

    def list_books(
    self,
    *,
    user_id: int,
    filters: BookFilters,
    page: int,
    size: int
) -> PaginatedResult[BookListItem]:

        offset = (page - 1) * size
        where_clauses = []
        params = []

        if filters.category:
            where_clauses.append("c.name = %s")
            params.append(filters.category)

        if filters.search:
            where_clauses.append("(b.title LIKE %s OR b.author LIKE %s)")
            params.extend([
                f"%{filters.search}%",
                f"%{filters.search}%"
            ])

        if filters.author:
            where_clauses.append("b.author LIKE %s")
            params.append(f"%{filters.author}%")

        where_sql = ""
        if where_clauses:
            where_sql = "WHERE " + " AND ".join(where_clauses)

        # ---------- COUNT ----------
        count_query = f"""
            SELECT COUNT(DISTINCT b.isbn)
            FROM books b
            JOIN categories c ON c.id = b.category_id
            {where_sql}
        """

        # ---------- DATA (USER-SCOPED) ----------
        data_query = f"""
            SELECT
                b.isbn,
                b.title,
                b.author,
                c.name AS category,
                b.cover_url,

                -- GLOBAL availability
                COALESCE(
                    SUM(CASE WHEN bc.status = 'available' THEN 1 ELSE 0 END),
                    0
                ) AS available_copies,

                -- USER-specific facts
                COUNT(DISTINCT br.id) AS user_active_borrow_count,
                COUNT(DISTINCT r.id)  AS user_active_reservation_count

            FROM books b
            JOIN categories c ON c.id = b.category_id
            LEFT JOIN book_copies bc
                ON bc.isbn = b.isbn

            LEFT JOIN borrowings br
                ON br.book_copy_id = bc.id
            AND br.returned_at IS NULL
            AND br.user_id = %s

            LEFT JOIN reservations r
                ON r.isbn = b.isbn
            AND r.status = 'active'
            AND r.user_id = %s

            {where_sql}
            GROUP BY
                b.isbn,
                b.title,
                b.author,
                c.name,
                b.cover_url
            ORDER BY b.created_at DESC
            LIMIT %s OFFSET %s
        """

        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        # COUNT
        cursor.execute(count_query, tuple(params))
        total = cursor.fetchone()["COUNT(DISTINCT b.isbn)"]

        # DATA
        cursor.execute(
            data_query,
            tuple([user_id, user_id] + params + [size, offset])
        )
        rows = cursor.fetchall()

        cursor.close()
        conn.close()

        items = [
            BookListItem(
                isbn=row["isbn"],
                title=row["title"],
                author=row["author"],
                category=row["category"],
                cover_url=row["cover_url"],
                available_copies=row["available_copies"],
                status=self._compute_status(row),
            )
            for row in rows
        ]

        return PaginatedResult(
            items=items,
            total=total,
            page=page,
            size=size,
        )



    def get_book_detail(
        self,
        isbn: str
    ) -> BookDetail | None:

        query = """
        SELECT
            b.isbn,
            b.title,
            b.author,
            b.description,
            c.name AS category
        FROM books b
        JOIN categories c ON c.id = b.category_id
        WHERE b.isbn = %s
        """

        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute(query, (isbn,))
        row = cursor.fetchone()
        cursor.close()

        if not row:
            return None

        return BookDetail(
            isbn=row["isbn"],
            title=row["title"],
            author=row["author"],
            description=row["description"],
            category=row["category"],
            available_copies=0,              # valeur par défaut OK
            status="unavailable",             # valeur par défaut OK
            is_favorite=False,                # valeur par défaut OK
        )


    def get_suggested_by_category(
    self,
    *,
    isbn: str,
    limit: int,
) -> list[BookListItem]:

        query = """
        SELECT
            b2.isbn,
            b2.title,
            b2.author,
            c.name AS category,
            b2.cover_url
        FROM books b1
        JOIN categories c ON c.id = b1.category_id
        JOIN books b2 ON b2.category_id = b1.category_id
        WHERE b1.isbn = %s
        AND b2.isbn != %s
        ORDER BY b2.created_at DESC
        LIMIT %s
        """

        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute(query, (isbn, isbn, limit))
        rows = cursor.fetchall()
        cursor.close()

        return [
            BookListItem(
                isbn=row["isbn"],
                title=row["title"],
                author=row["author"],
                category=row["category"],
                cover_url=row["cover_url"],
            )
            for row in rows
        ]

    # ---------- USER PAGES ----------

    async def list_favorite_books(
        self,
        *,
        user_id: int
    ) -> list[BookListItem]:

        query = """
        SELECT
            b.isbn,
            b.title,
            b.author,
            c.name AS category,
            b.cover_url
        FROM favorites f
        JOIN books b ON b.isbn = f.isbn
        JOIN categories c ON c.id = b.category_id
        WHERE f.user_id = :user_id
        ORDER BY f.created_at DESC
        """

        conn =  get_connection()
        rows =  conn.fetch_all(query, {"user_id": user_id})

        return [
            BookListItem(
                isbn=row["isbn"],
                title=row["title"],
                author=row["author"],
                category=row["category"],
                cover_url=row["cover_url"],
            )
            for row in rows
        ]

    async def list_borrowing_history(
        self,
        *,
        user_id: int
    ) -> list[BookListItem]:

        query = """
        SELECT DISTINCT
            b.isbn,
            b.title,
            b.author,
            c.name AS category,
            b.cover_url
        FROM borrowings br
        JOIN book_copies bc ON bc.id = br.book_copy_id
        JOIN books b ON b.isbn = bc.isbn
        JOIN categories c ON c.id = b.category_id
        WHERE br.user_id = :user_id
        ORDER BY br.borrowed_at DESC
        """

        conn = await get_connection()
        rows = await conn.fetch_all(query, {"user_id": user_id})

        return [
            BookListItem(
                isbn=row["isbn"],
                title=row["title"],
                author=row["author"],
                category=row["category"],
                cover_url=row["cover_url"],
            )
            for row in rows
        ]

    # ---------- INTERNAL ----------

    async def exists_by_isbn(self, *, isbn: str) -> bool:
        query = "SELECT 1 FROM books WHERE isbn = :isbn LIMIT 1"

        conn = await get_connection()
        value = await conn.fetch_val(query, {"isbn": isbn})

        return value is not None

    def get_suggested_books(
    self,
    *,
    isbn: str,
    limit: int
) -> list[BookListItem]:
        # This method is not used by the application directly, but it's part of the interface.
        # The actual suggestion logic is in get_suggested_by_category() for now.
        return self.get_suggested_by_category(isbn=isbn, limit=limit)