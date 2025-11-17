class SearchService:
    @staticmethod
    def search_movies(query: str, movies: list) -> list:
        """
        简化版搜索：对 title/genres/actors 拼成的文本做子串匹配。
        多关键词按 AND。
        """
        q = (query or "").strip().lower()
        if not q:
            return []
        parts = q.split()
        results = []
        for m in movies:
            hay = " ".join([
                m.get("title", ""),
                " ".join(m.get("genres", [])),
                " ".join(m.get("actors", [])),
            ]).lower()
            if all(p in hay for p in parts):
                results.append(m)
        return results