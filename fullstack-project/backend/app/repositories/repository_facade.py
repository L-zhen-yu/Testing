from app.models.user import User
from app.models.movie import Movie
from app.models.review import Review


class RepositoryFacade:
    def __init__(self):
        self.users = {}
        self.movies = {}

    def registerUser(self, username, password):
        if username in self.users:
            return "User exists"
        self.users[username] = User(username, password)
        return "Registered"

    def add_movie(self, title):
        if title not in self.movies:
            self.movies[title] = Movie(title)
        return self.movies[title]

    def add_review(self, username, movie_title, review_text, rating):
        if username not in self.users:
            return "User not found"
        movie = self.add_movie(movie_title)
        review = Review(review_text)
        movie.addReview(review, rating)
        return "Review added"
