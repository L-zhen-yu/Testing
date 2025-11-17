import unittest
from app.models.User_class import User, role_enum, status_enum
from app.models.movies import Movie
from app.repositories.movie_repo import InMemoryMovieRepo
from app.services.review_flow import ReviewService

class TestIntegrationUserMovieRating(unittest.TestCase):
    def test_add_review_updates_movie_average(self):
        # Arrange: user + repo + movie
        user = User()
        user.constructor("u1", "Zhenyu", "hash", role_enum.user, status_enum.active)
        repo = InMemoryMovieRepo()
        repo.add(Movie("m1", "Inception"))  # with 0 rating
        service = ReviewService(repo)

        # Act: add a 7.5 and a 8.5
        service.add_review(user, "m1", 7.5, "nice")
        service.add_review(user, "m1", 8.5, "great")

        # Assert: the rating number should be 2 and the average score should be 8.0
        m = repo.get("m1")
        self.assertEqual(len(m.ratings), 2)
        self.assertAlmostEqual(m.average, 8.0, places=6)

if __name__ == "__main__":
    unittest.main()
