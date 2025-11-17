from app.models.movies import Movie

class InMemoryMovieRepo:
    def __init__(self):
        self._store: dict[str, Movie] = {}

    def add(self, movie: Movie):
        self._store[movie.movieId] = movie

    def get(self, movie_id: str) -> Movie:
        return self._store[movie_id]

    def save(self, movie: Movie):
        self._store[movie.movieId] = movie