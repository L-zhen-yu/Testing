# backend/app/routers/ratings.py
from fastapi import APIRouter, Depends, HTTPException, status
from app.schemas.ratings import RatingCreate, RatingOut, RatingSummary
#from app.services.ratings_service import RatingsService

# 依赖：拿到 storage 与当前用户
#from app.deps import auth_deps  # 你的项目里已有此模块
#from app.storage.json_adapter import JsonAdapter  # 如果你封装在别处，请按实际改

# router = APIRouter(prefix="/ratings", tags=["ratings"])

# def get_storage():
#     # 按你项目里实际的 data 目录调整
#     # 如果你有统一的 Settings，这里应从 config 读取
#     return JsonAdapter(base_dir="app/data")

# def get_service(storage=Depends(get_storage)):
#     return RatingsService(storage)

# @router.post("/{movie_id}", response_model=RatingOut, status_code=201)
# def create_or_update_rating(
#     movie_id: str,
#     payload: RatingCreate,
#     current_user: dict = Depends(auth_deps.get_current_user),  # 如果你的是 require_user，请替换
#     svc: RatingsService = Depends(get_service),
# ):
#     """
#     Upsert rating for (current_user, movie_id).
#     Score must be in [1..10] with 0.5 steps.
#     """
#     try:
#         r = svc.upsert_rating(current_user, movie_id, payload.score)
#         return r
#     except ValueError as e:
#         raise HTTPException(status_code=404, detail=str(e))
#     except Exception as e:
#         raise HTTPException(status_code=500, detail="Failed to save rating")

# @router.get("/me/{movie_id}", response_model=RatingOut)
# def get_my_rating(
#     movie_id: str,
#     current_user: dict = Depends(auth_deps.get_current_user),
#     svc: RatingsService = Depends(get_service),
# ):
#     r = svc.get_user_rating(current_user["id"], movie_id)
#     if not r:
#         raise HTTPException(status_code=404, detail="Rating not found")
#     return r

# @router.get("/summary/{movie_id}", response_model=RatingSummary)
# def get_rating_summary(
#     movie_id: str,
#     svc: RatingsService = Depends(get_service),
# ):
#     avg, cnt = svc.compute_summary(movie_id)
#     return RatingSummary(movie_id=movie_id, average=round(avg, 2), count=cnt)
