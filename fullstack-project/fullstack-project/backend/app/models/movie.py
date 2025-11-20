class Movie:
    def __init__(self, title):
        self.title = title
        self.reviews = []
        self.ratings = []

    def addReview(self, review, rating):
        self.reviews.append(review)
        self.ratings.append(rating)

    def calculateAverageRating(self):
        if not self.ratings:
            return 0
        return round(sum(self.ratings) / len(self.ratings), 1)
