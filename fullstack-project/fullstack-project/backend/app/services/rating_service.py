# app/services/rating_service.py
from __future__ import annotations

from typing import List

from fastapi import HTTPException, status

from app.schemas.rating_schema import RatingCreate, RatingOut
from app.repositories import rating_repository


class RatingService:
    """
    评分相关的业务逻辑。
    """

    def create_or_update_rating(self, *, user_id: str, rating_in: RatingCreate) -> RatingOut:
        # 这里本来可以检查 movie_id 是否存在（看 data 里是否有这个电影目录）
        stored = rating_repository.upsert_rating(
            user_id=user_id,
            movie_id=rating_in.movie_id,
            score=rating_in.score,
        )
        return RatingOut(**stored)

    def get_ratings_for_movie(self, movie_id: str) -> List[RatingOut]:
        items = rating_repository.get_ratings_for_movie(movie_id)
        return [RatingOut(**i) for i in items]

    def get_ratings_for_user(self, user_id: str) -> List[RatingOut]:
        items = rating_repository.get_ratings_for_user(user_id)
        return [RatingOut(**i) for i in items]

    def delete_rating(self, *, user_id: str, movie_id: str) -> None:
        deleted = rating_repository.delete_rating(user_id=user_id, movie_id=movie_id)
        if not deleted:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Rating not found",
            )
