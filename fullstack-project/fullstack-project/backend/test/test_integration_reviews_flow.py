import unittest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.models.user import User
from app.models.movies import Movie
from app.repositories.movie_repo import InMemoryMovieRepo
from app.services.review_flow import ReviewService
from app.models.userMethods import save_users

# --------------------------------------------------------------
# FastAPI app that wires User + ReviewService + Movie repository
# --------------------------------------------------------------

app = FastAPI()

# Global objects used by the endpoints and reset between tests
repo = InMemoryMovieRepo()
repo.add(Movie("m1", "Inception"))
service = ReviewService(repo)
current_user = User()


@app.post("/integration/reset")
def reset_state():
    """
    Reset the in-memory repository, service and user instance,
    and clear the users.json file so tests start from a clean state.
    """
    global repo, service, current_user
    repo = InMemoryMovieRepo()
    repo.add(Movie("m1", "Inception"))
    service = ReviewService(repo)
    current_user = User()
    # Clear persisted users so signup behaves consistently
    save_users({})
    return {"detail": "reset"}


@app.post("/integration/setup-user")
def setup_user(username: str = "u1", password: str = "Abc12345"):
    """
    Helper endpoint: create and log in a normal user via User.signup().
    """
    message = current_user.signup(username, password)
    return {
        "message": message,
        "username": current_user.username,
        "logged_in": current_user.logged_in,
        "is_admin": current_user.is_admin,
        "is_banned": current_user.is_banned,
    }


@app.post("/integration/add-review")
def add_review(score: float, text: str = "nice", movie_id: str = "m1"):
    """
    Add a review for a movie using the current User and ReviewService.
    If the user is not logged in yet, set up a default one.
    """
    global current_user
    if not current_user.logged_in:
        current_user.signup("u1", "Abc12345")
    service.add_review(current_user, movie_id, score, text)
    return {"detail": "ok"}


@app.get("/integration/movie/{movie_id}")
def get_movie(movie_id: str):
    """
    Expose aggregated rating information for the given movie.
    """
    m = repo.get(movie_id)
    return {
        "rating_count": len(m.ratings),
        "average": m.average,
    }


client = TestClient(app)


class TestIntegrationUserMovieRatingAPI(unittest.TestCase):
    def setUp(self):
        # Ensure clean state and a logged-in user before each test
        client.post("/integration/reset")
        client.post("/integration/setup-user")

    def test_add_review_updates_movie_average(self):
        """
        Integration test:
        After adding two reviews (7.5 and 8.5) from the same user,
        the movie should have 2 ratings and an average of 8.0.
        """
        resp1 = client.post(
            "/integration/add-review",
            params={"score": 7.5, "text": "nice"},
        )
        self.assertEqual(resp1.status_code, 200)

        resp2 = client.post(
            "/integration/add-review",
            params={"score": 8.5, "text": "great"},
        )
        self.assertEqual(resp2.status_code, 200)

        movie_resp = client.get("/integration/movie/m1")
        self.assertEqual(movie_resp.status_code, 200)
        data = movie_resp.json()
        self.assertEqual(data["rating_count"], 2)
        self.assertAlmostEqual(data["average"], 8.0, places=6)


if __name__ == "__main__":
    unittest.main()
