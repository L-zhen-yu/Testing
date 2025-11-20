# app/services/favorites_service.py
from __future__ import annotations

from typing import List

from fastapi import HTTPException, status

from app.schemas.favorite_schema import FavoriteCreate, FavoriteOut
from app.repositories import favorites_repository


class FavoriteService:
    """
    收藏列表的业务逻辑。
    """

    def add_favorite(self, *, user_id: str, fav_in: FavoriteCreate) -> FavoriteOut:
        stored = favorites_repository.add_favorite(
            user_id=user_id,
            movie_id=fav_in.movie_id,
        )
        return FavoriteOut(**stored)

    def remove_favorite(self, *, user_id: str, movie_id: str) -> None:
        deleted = favorites_repository.remove_favorite(
            user_id=user_id,
            movie_id=movie_id,
        )
        if not deleted:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Favorite not found",
            )

    def list_favorites_for_user(self, user_id: str) -> List[FavoriteOut]:
        items = favorites_repository.list_favorites_for_user(user_id)
        return [FavoriteOut(**i) for i in items]
