# app/schemas/rating_schema.py
from __future__ import annotations

from typing import List
from pydantic import BaseModel, Field, validator


class RatingBase(BaseModel):
    movie_id: str = Field(..., description="Movie ID being rated")


class RatingCreate(RatingBase):
    score: float = Field(..., description="Rating from 1.0 to 10.0 in 0.5 steps")

    @validator("score")
    def validate_score(cls, v: float) -> float:
        if v < 1.0 or v > 10.0:
            raise ValueError("score must be between 1.0 and 10.0")
        # 强制 0.5 步长：score * 2 必须是整数
        if abs(v * 2 - round(v * 2)) > 1e-6:
            raise ValueError("score must be in steps of 0.5")
        return v


class RatingOut(RatingBase):
    user_id: str
    score: float
    created_at: str | None = None
    updated_at: str | None = None


class RatingList(BaseModel):
    items: List[RatingOut]
