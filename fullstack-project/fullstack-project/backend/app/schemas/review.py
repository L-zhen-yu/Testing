from pydantic import BaseModel
from typing import Optional

class ReviewBase(BaseModel):
    rating: int
    comment: Optional[str] = None

class ReviewCreate(ReviewBase):
    user_id: int
    item_id: int

class Review(ReviewBase):
    id: int
    user_id: int
    item_id: int
