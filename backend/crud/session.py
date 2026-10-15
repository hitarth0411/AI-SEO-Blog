import secrets
from datetime import datetime, timedelta

from pymongo.database import Database

from core.database import get_next_id
from models.session import Session as SessionModel


def _to_session(document: dict | None) -> SessionModel | None:
    if document is None:
        return None
    return SessionModel(
        id=document["_id"],
        session_token=document["session_token"],
        user_id=document["user_id"],
        created_at=document["created_at"],
        last_access_at=document["last_access_at"],
        expires_at=document["expires_at"],
    )


def create_session(
    db: Database, *, user_id: int, ttl_days: int = 30
) -> SessionModel:
    now = datetime.utcnow()
    session = SessionModel(
        id=get_next_id(db, "sessions"),
        session_token=secrets.token_urlsafe(32),
        user_id=user_id,
        created_at=now,
        last_access_at=now,
        expires_at=now + timedelta(days=ttl_days),
    )
    db.sessions.insert_one(
        {
            "_id": session.id,
            "session_token": session.session_token,
            "user_id": session.user_id,
            "created_at": session.created_at,
            "last_access_at": session.last_access_at,
            "expires_at": session.expires_at,
        }
    )
    return session


def get_session_by_token(db: Database, token: str) -> SessionModel | None:
    return _to_session(db.sessions.find_one({"session_token": token}))


def update_session_last_access(
    db: Database, session_id: int, when: datetime
) -> None:
    db.sessions.update_one(
        {"_id": session_id},
        {"$set": {"last_access_at": when}},
    )


def delete_session(db: Database, session: SessionModel) -> None:
    db.sessions.delete_one({"_id": session.id})
