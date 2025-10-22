class RatingService:
    """
    评分规则：1.0 <= score <= 10.0 且步长 0.5
    返回 True 表示通过；否则抛 ValueError。
    """
    @staticmethod
    def validate_score(score: float) -> bool:
        if not isinstance(score, (int, float)):
            raise ValueError("score must be number")
        if score < 1.0 or score > 10.0:
            raise ValueError("out of range")
        # 步长 0.5：乘以 2 后应为整数
        if (score * 2) % 1 != 0:
            raise ValueError("step must be 0.5")
        return True