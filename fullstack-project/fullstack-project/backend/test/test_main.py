from app.models.user import User
from app.repositories.repository_facade import RepositoryFacade



    
from fastapi import FastAPI
from app.repositories.repository_facade import RepositoryFacade

app = FastAPI()
repo = RepositoryFacade()

@app.get("/")
def home():
    return {"msg": "Welcome to ByteMe API"}

@app.post("/register/{username}/{password}")
def register_user(username: str, password: str):
    result = repo.registerUser(username, password)
    return {"result": result}

@app.post("/review/{username}/{movie_title}")
def add_review(username: str, movie_title: str, review: str = "Great movie!", rating: int = 5):
    result = repo.add_review(username, movie_title, review, rating)
    return {"result": result}
