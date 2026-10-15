from dataclasses import dataclass
from datetime import datetime


@dataclass
class Blog:
    id: int
    title: str
    content: str
    keywords: str
    created_at: datetime
    user_id: int | None = None
