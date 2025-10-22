import unittest
from app.services.search_service import SearchService

MOVIES = [
    {"title": "Inception", "genres": ["Sci-Fi"], "actors": ["Leonardo DiCaprio"]},
    {"title": "Se7en", "genres": ["Crime", "Thriller"], "actors": ["Brad Pitt"]},
    {"title": "Star Wars", "genres": ["Sci-Fi"], "actors": ["Mark Hamill"]},
]

class TestSearchService(unittest.TestCase):
    def test_empty_query_returns_empty(self):
        self.assertEqual(SearchService.search_movies("", MOVIES), [])
        self.assertEqual(SearchService.search_movies("   ", MOVIES), [])

    def test_single_keyword(self):
        res = SearchService.search_movies("inception", MOVIES)
        self.assertEqual(len(res), 1)
        self.assertEqual(res[0]["title"], "Inception")

    def test_multi_keywords_and_semantics(self):
        # "star war" 两个词都匹配到 "Star Wars"
        res = SearchService.search_movies("star war", MOVIES)
        self.assertEqual(len(res), 1)
        self.assertEqual(res[0]["title"], "Star Wars")


    def test_no_match(self):
        self.assertEqual(SearchService.search_movies("nonexistent", MOVIES), [])



    def test_special_characters(self):
        res = SearchService.search_movies("Se7en", MOVIES)
        self.assertEqual(len(res), 1)
        self.assertEqual(res[0]["title"], "Se7en")


if __name__ == "__main__":
    unittest.main()