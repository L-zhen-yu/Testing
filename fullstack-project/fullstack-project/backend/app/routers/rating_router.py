# app/routers/rating_router.py
from __future__ import annotations

from fastapi import APIRouter, Depends

from app.schemas.rating_schema import RatingCreate, RatingOut, RatingList
from app.services.rating_service import RatingService

router = APIRouter(prefix="/ratings", tags=["ratings"])

_service = RatingService()


def get_rating_service() -> RatingService:
    return _service


@router.post(
    "/users/{user_id}",
    response_model=RatingOut,
    summary="Create or update rating for a movie",
)
def create_or_update_rating(
    user_id: str,
    rating_in: RatingCreate,
    svc: RatingService = Depends(get_rating_service),
):
    """
    为某个电影创建/更新用户评分。
    NOTE: 正式版建议不要把 user_id 放 URL，而是从 auth 中拿当前用户。
    """
    return svc.create_or_update_rating(user_id=user_id, rating_in=rating_in)


@router.get(
    "/movie/{movie_id}",
    response_model=RatingList,
    summary="Get all ratings for a movie",
)
def list_ratings_for_movie(
    movie_id: str,
    svc: RatingService = Depends(get_rating_service),
):
    items = svc.get_ratings_for_movie(movie_id)
    return RatingList(items=items)


@router.get(
    "/user/{user_id}",
    response_model=RatingList,
    summary="Get all ratings by a user",
)
def list_ratings_for_user(
    user_id: str,
    svc: RatingService = Depends(get_rating_service),
):
    items = svc.get_ratings_for_user(user_id)
    return RatingList(items=items)


@router.delete(
    "/users/{user_id}/movies/{movie_id}",
    summary="Delete a rating for a movie by user",
)
def delete_rating(
    user_id: str,
    movie_id: str,
    svc: RatingService = Depends(get_rating_service),
):
    svc.delete_rating(user_id=user_id, movie_id=movie_id)
    return {"detail": "Rating deleted"}
