# backend/app/schemas/ratings.py
from pydantic import BaseModel, field_validator
from typing import Optional
from datetime import datetime

ALLOWED_MIN = 1.0
ALLOWED_MAX = 10.0

class RatingBase(BaseModel):
    score: float

    @field_validator("score")
    @classmethod
    def validate_score(cls, v: float) -> float:
        # must be in [1.0, 10.0] with 0.5 step
        if not (ALLOWED_MIN <= v <= ALLOWED_MAX):
            raise ValueError("Score must be between 1.0 and 10.0")
        # step of 0.5 => 2*score is integer
        if abs(v * 2 - round(v * 2)) > 1e-9:
            raise ValueError("Score must step by 0.5 (e.g., 7, 7.5, 8)")
        return float(v)

class RatingCreate(RatingBase):
    pass

class RatingOut(BaseModel):
    id: str
    movie_id: str
    user_id: str
    score: float
    created_at: datetime
    updated_at: Optional[datetime] = None

class RatingSummary(BaseModel):
    movie_id: str
    average: float
    count: int
