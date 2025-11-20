# app/routers/favorites_router.py
from __future__ import annotations

from fastapi import APIRouter, Depends

from app.schemas.favorite_schema import FavoriteCreate, FavoriteOut, FavoriteList
from app.services.favorites_service import FavoriteService

router = APIRouter(prefix="/favorites", tags=["favorites"])

_service = FavoriteService()


def get_favorite_service() -> FavoriteService:
    return _service


@router.post(
    "/users/{user_id}",
    response_model=FavoriteOut,
    summary="Add movie to user's favorites",
)
def add_favorite(
    user_id: str,
    fav_in: FavoriteCreate,
    svc: FavoriteService = Depends(get_favorite_service),
):
    return svc.add_favorite(user_id=user_id, fav_in=fav_in)


@router.delete(
    "/users/{user_id}/movies/{movie_id}",
    summary="Remove movie from user's favorites",
)
def remove_favorite(
    user_id: str,
    movie_id: str,
    svc: FavoriteService = Depends(get_favorite_service),
):
    svc.remove_favorite(user_id=user_id, movie_id=movie_id)
    return {"detail": "Favorite removed"}


@router.get(
    "/users/{user_id}",
    response_model=FavoriteList,
    summary="List user's favorites",
)
def list_favorites(
    user_id: str,
    svc: FavoriteService = Depends(get_favorite_service),
):
    items = svc.list_favorites_for_user(user_id)
    return FavoriteList(items=items)
