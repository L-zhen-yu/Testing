from dataclasses import dataclass, field

@dataclass
class Movie:
    movieId: str
    title: str
    ratings: list = field(default_factory=list)
    average: float = 0.0

    def add_score(self, score: float):
        self.ratings.append(score)
        self.average = sum(self.ratings) / len(self.ratings)