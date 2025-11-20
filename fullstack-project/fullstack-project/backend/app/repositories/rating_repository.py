# app/repositories/rating_repository.py
from __future__ import annotations

from typing import List, Dict, Optional
from datetime import datetime, timezone

from app.repositories import base

RATINGS_FILE = "ratings.json"


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _load_all() -> List[Dict]:
    data = base.load_json(RATINGS_FILE)
    if isinstance(data, list):
        return data
    return []


def _save_all(items: List[Dict]) -> None:
    base.save_json(RATINGS_FILE, items)


def upsert_rating(*, user_id: str, movie_id: str, score: float) -> Dict:
    """
    新建或更新评分：每个 (user_id, movie_id) 只能有一个评分。
    返回存储后的 rating dict。
    """
    items = _load_all()
    for item in items:
        if item["user_id"] == user_id and item["movie_id"] == movie_id:
            item["score"] = score
            item["updated_at"] = _now_iso()
            _save_all(items)
            return item

    now = _now_iso()
    new_item = {
        "user_id": user_id,
        "movie_id": movie_id,
        "score": score,
        "created_at": now,
        "updated_at": now,
    }
    items.append(new_item)
    _save_all(items)
    return new_item


def get_rating(user_id: str, movie_id: str) -> Optional[Dict]:
    for item in _load_all():
        if item["user_id"] == user_id and item["movie_id"] == movie_id:
            return item
    return None


def get_ratings_for_movie(movie_id: str) -> List[Dict]:
    return [item for item in _load_all() if item["movie_id"] == movie_id]


def get_ratings_for_user(user_id: str) -> List[Dict]:
    return [item for item in _load_all() if item["user_id"] == user_id]


def delete_rating(user_id: str, movie_id: str) -> bool:
    items = _load_all()
    new_items = [
        i for i in items
        if not (i["user_id"] == user_id and i["movie_id"] == movie_id)
    ]
    if len(new_items) == len(items):
        return False
    _save_all(new_items)
    return True
