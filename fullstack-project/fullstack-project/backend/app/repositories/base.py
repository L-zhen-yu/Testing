# app/repositories/base.py
from pathlib import Path
from typing import Any
import json

# 所有数据文件的根目录
# 在测试里可以 monkeypatch 这个 DATA_DIR 到 tmp_path
DATA_DIR: Path = Path(__file__).resolve().parents[1] / "data"


def _ensure_data_dir() -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)


def load_json(filename: str) -> Any:
    """
    从 DATA_DIR / filename 加载 JSON。
    文件不存在或坏掉时，返回 []，避免直接崩。
    """
    _ensure_data_dir()
    path = DATA_DIR / filename
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []


def save_json(filename: str, data: Any) -> None:
    """
    把任意可 JSON 序列化的数据写入 DATA_DIR / filename。
    """
    _ensure_data_dir()
    path = DATA_DIR / filename
    with path.open("w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
