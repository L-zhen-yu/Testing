from app.services.rating_service import RatingService

class ReviewService:
    """
    演示用的“集成链路”服务：校验评分 → 写入电影 → 更新平均分
    真实项目里你可以把它合并进更大的 Service 或 Facade。
    """
    def __init__(self, movie_repo):
        self.movie_repo = movie_repo

    def add_review(self, user, movie_id: str, score: float, text: str = ""):
        # 1) 校验评分
        RatingService.validate_score(score)
        # 2) 获取电影对象并写入评分
        movie = self.movie_repo.get(movie_id)
        movie.add_score(score)
        # 3) 保存（模拟持久化）
        self.movie_repo.save(movie)
        # 4) 返回最小结果（真实项目里可返回 Review 对象/DTO）
        return {"movieId": movie_id, "userId": user.userId, "score": score, "text": text}