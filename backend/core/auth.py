from datetime import datetime

from fastapi import Depends, Header, HTTPException
from pymongo.database import Database

from core.database import database
from crud.session import get_session_by_token, update_session_last_access
from crud.user import get_user_by_id
from fastapi.security import OAuth2PasswordBearer
from models.user import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/signin")


def get_db() -> Database:
    return database


def _parse_bearer_token(authorization: str | None) -> str:
    if not authorization:
        raise HTTPException(status_code=401, detail="Missing Authorization header")
    parts = authorization.split()
    if len(parts) != 2 or parts[0].lower() != "bearer":
        raise HTTPException(status_code=401, detail="Invalid Authorization header")
    return parts[1]


def get_current_user_optional(
    authorization: str | None = Header(default=None),
    db: Database = Depends(get_db),
) -> User | None:
    if not authorization:
        return None

    try:
        token = _parse_bearer_token(authorization)
    except HTTPException:
        return None

    session = get_session_by_token(db, token)
    if not session or session.expires_at < datetime.utcnow():
        return None

    now = datetime.utcnow()
    update_session_last_access(db, session.id, now)

    user = get_user_by_id(db, session.user_id)
    if not user or not user.is_active:
        return None

    return user


def get_current_user(
    authorization: str | None = Header(default=None),
    db: Database = Depends(get_db),
) -> User:
    token = _parse_bearer_token(authorization)
    session = get_session_by_token(db, token)
    if not session or session.expires_at < datetime.utcnow():
        raise HTTPException(status_code=401, detail="Invalid or expired session")

    update_session_last_access(db, session.id, datetime.utcnow())

    user = get_user_by_id(db, session.user_id)
    if not user or not user.is_active:
        raise HTTPException(status_code=401, detail="User is inactive")

    return user
