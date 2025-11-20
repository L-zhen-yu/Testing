# backend/app/repositories/ratings_repo.py
from __future__ import annotations
from typing import List, Optional, Dict, Any
from datetime import datetime, timezone

# 假设你的 storage adapter 暴露成单例或通过工厂拿到，这里演示传入方式
# 你可以在 app/services/ratings_service.py 里注入 storage，再传给本仓储
class RatingsRepository:
    def __init__(self, storage, collection_name: str = "ratings"):
        """
        storage: an adapter with read(name) -> list[dict], write(name, list[dict]) -> None
        """
        self.storage = storage
        self.collection = collection_name

    def _read_all(self) -> List[Dict[str, Any]]:
        try:
            return list(self.storage.read(self.collection))
        except FileNotFoundError:
            return []

    def _write_all(self, rows: List[Dict[str, Any]]) -> None:
        self.storage.write(self.collection, rows)

    def list_by_movie(self, movie_id: str) -> List[Dict[str, Any]]:
        rows = self._read_all()
        return [r for r in rows if r.get("movie_id") == movie_id]

    def get_by_user_and_movie(self, user_id: str, movie_id: str) -> Optional[Dict[str, Any]]:
        rows = self._read_all()
        for r in rows:
            if r.get("user_id") == user_id and r.get("movie_id") == movie_id:
                return r
        return None

    @staticmethod
    def make_id(movie_id: str, user_id: str) -> str:
        # one rating per (user, movie) → deterministic id
        return f"rat_{movie_id}_{user_id}"

    def upsert(self, user_id: str, movie_id: str, score: float) -> Dict[str, Any]:
        rows = self._read_all()
        now = datetime.now(timezone.utc).isoformat()
        rid = self.make_id(movie_id, user_id)

        # try update
        updated = False
        for r in rows:
            if r.get("id") == rid:
                r["score"] = float(score)
                r["updated_at"] = now
                updated = True
                result = r
                break

        if not updated:
            result = {
                "id": rid,
                "movie_id": movie_id,
                "user_id": user_id,
                "score": float(score),
                "created_at": now,
                "updated_at": None,
            }
            rows.append(result)

        self._write_all(rows)
        return result
