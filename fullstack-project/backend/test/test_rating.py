import unittest
from app.services.rating_service import RatingService

class TestRatingValidation(unittest.TestCase):
    def test_valid_scores(self):
        for s in [1.0, 7.5, 10.0]:
            self.assertTrue(RatingService.validate_score(s))

    def test_invalid_scores_out_of_range(self):
        for s in [0.0, 10.5]:
            with self.assertRaises(ValueError):
                RatingService.validate_score(s)

    def test_invalid_step(self):
        with self.assertRaises(ValueError):
            RatingService.validate_score(7.3)

if __name__ == "__main__":
    unittest.main()