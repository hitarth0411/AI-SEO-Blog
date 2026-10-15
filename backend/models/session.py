from dataclasses import dataclass
from datetime import datetime


@dataclass
class Session:
    id: int
    session_token: str
    user_id: int
    created_at: datetime
    last_access_at: datetime
    expires_at: datetime
