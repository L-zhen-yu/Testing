from fastapi import FastAPI
# import rating and favorites routers
from app.routers import rating_router, favorites_router

app = FastAPI()
@app.get("/health")
def health():
    return {"status": ok}



app = FastAPI(title="Movie Review System")

# 原有的 app.include_router(...)
app.include_router(rating_router.router)
app.include_router(favorites_router.router)

