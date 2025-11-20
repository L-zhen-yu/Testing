import unittest
from fastapi import FastAPI, HTTPException
from fastapi.testclient import TestClient

from app.services.rating_service import RatingService

# --- FastAPI app exposing a validation endpoint for ratings ---

app = FastAPI()


@app.get("/rating/validate")
def validate_rating(score: float):
    """
    Wrap RatingService.validate_score(score) as an HTTP endpoint.

    If the score is invalid, propagate the error as HTTP 400.
    """
    try:
        RatingService.validate_score(score)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return {"ok": True}


client = TestClient(app)


class TestRatingValidationAPI(unittest.TestCase):
    def test_valid_scores(self):
        """
        Valid partition: scores inside [1.0, 10.0] with step 0.5.
        """
        for s in [1.0, 7.5, 10.0]:
            resp = client.get("/rating/validate", params={"score": s})
            self.assertEqual(resp.status_code, 200)
            self.assertEqual(resp.json()["ok"], True)

    def test_invalid_scores_out_of_range(self):
        """
        Out-of-range partition: below 1.0 or above 10.0.
        """
        for s in [0.0, 10.5]:
            resp = client.get("/rating/validate", params={"score": s})
            self.assertEqual(resp.status_code, 400)

    def test_invalid_step(self):
        """
        Wrong-step partition: score that does not follow 0.5 increments.
        """
        resp = client.get("/rating/validate", params={"score": 7.3})
        self.assertEqual(resp.status_code, 400)


if __name__ == "__main__":
    unittest.main()
