# app/repositories/favorites_repository.py
from __future__ import annotations

from typing import List, Dict

from app.repositories import base

FAVORITES_FILE = "favorites.json"


def _load_all() -> List[Dict]:
    data = base.load_json(FAVORITES_FILE)
    if isinstance(data, list):
        return data
    return []


def _save_all(items: List[Dict]) -> None:
    base.save_json(FAVORITES_FILE, items)


def add_favorite(*, user_id: str, movie_id: str) -> Dict:
    """
    添加收藏。如果已经存在，直接返回原条目。
    """
    items = _load_all()
    for item in items:
        if item["user_id"] == user_id and item["movie_id"] == movie_id:
            return item

    new_item = {"user_id": user_id, "movie_id": movie_id}
    items.append(new_item)
    _save_all(items)
    return new_item


def remove_favorite(*, user_id: str, movie_id: str) -> bool:
    items = _load_all()
    new_items = [
        i for i in items
        if not (i["user_id"] == user_id and i["movie_id"] == movie_id)
    ]
    if len(new_items) == len(items):
        return False
    _save_all(new_items)
    return True


def list_favorites_for_user(user_id: str) -> List[Dict]:
    return [i for i in _load_all() if i["user_id"] == user_id]
