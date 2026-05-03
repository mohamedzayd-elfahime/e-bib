from app.application.read_models.favorite import FavoriteIn
from fastapi import (
    APIRouter,
    Depends,
)

from app.application.use_cases.toggle_favorite import ToggleFavorite
from app.presentation.api.dependencies import (
    get_current_user_id,
    get_favorite_repository,
)

router = APIRouter()
@router.post("/favorites")
async def toggle_favorite(
    payload: FavoriteIn,
    user_id: int = Depends(get_current_user_id),
    repo = Depends(get_favorite_repository),
):
    status = ToggleFavorite(repo).execute(user_id, payload.isbn)
    return {"status": status}
