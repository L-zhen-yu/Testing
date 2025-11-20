import unittest
from fastapi import FastAPI, Query
from fastapi.testclient import TestClient

from app.services.search_service import SearchService

# Small in-memory movie list for the tests
MOVIES = [
    {"title": "Inception", "genres": ["Sci-Fi"], "actors": ["Leonardo DiCaprio"]},
    {"title": "Se7en", "genres": ["Crime", "Thriller"], "actors": ["Brad Pitt"]},
    {"title": "Star Wars", "genres": ["Sci-Fi"], "actors": ["Mark Hamill"]},
]

# --- FastAPI app exposing the search endpoint used by the tests ---

app = FastAPI()


@app.get("/search")
def search_movies(q: str = Query("")):
    """
    Wrap SearchService.search_movies as an HTTP endpoint.
    """
    results = SearchService.search_movies(q, MOVIES)
    return {"results": results}


client = TestClient(app)


class TestSearchServiceAPI(unittest.TestCase):
    def test_empty_query_returns_empty(self):
        """
        Case 3-1: empty / whitespace-only query → early exit branch.
        """
        resp = client.get("/search", params={"q": ""})
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json()["results"], [])

        resp = client.get("/search", params={"q": "   "})
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json()["results"], [])

    def test_single_keyword(self):
        """
        Case 3-2: single keyword should return one match.
        """
        resp = client.get("/search", params={"q": "inception"})
        self.assertEqual(resp.status_code, 200)
        data = resp.json()["results"]
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["title"], "Inception")

    def test_multi_keywords_and_semantics(self):
        """
        Case 3-3: multi-keyword AND semantics, e.g. 'star war'.
        """
        resp = client.get("/search", params={"q": "star war"})
        self.assertEqual(resp.status_code, 200)
        data = resp.json()["results"]
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["title"], "Star Wars")

    def test_no_match(self):
        """
        Case 3-4: query that matches no movie.
        """
        resp = client.get("/search", params={"q": "nonexistent"})
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json()["results"], [])

    def test_special_characters(self):
        """
        Extra case: title containing special characters, such as 'Se7en'.
        """
        resp = client.get("/search", params={"q": "Se7en"})
        self.assertEqual(resp.status_code, 200)
        data = resp.json()["results"]
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["title"], "Se7en")


if __name__ == "__main__":
    unittest.main()
