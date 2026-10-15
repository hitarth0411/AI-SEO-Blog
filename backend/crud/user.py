from datetime import datetime

import bcrypt
from pymongo.database import Database

from core.database import get_next_id
from models.user import User


def _to_user(document: dict | None) -> User | None:
    if document is None:
        return None
    return User(
        id=document["_id"],
        name=document["name"],
        email=document["email"],
        password_salt=document["password_salt"],
        password_hash=document["password_hash"],
        role=document["role"],
        is_active=document["is_active"],
        created_at=document["created_at"],
        updated_at=document["updated_at"],
        last_login_at=document.get("last_login_at"),
    )


def create_user(db: Database, *, name: str, email: str, password: str) -> User:
    now = datetime.utcnow()
    salt = bcrypt.gensalt()
    user = User(
        id=get_next_id(db, "users"),
        name=name,
        email=email,
        password_salt=salt.decode("utf-8"),
        password_hash=bcrypt.hashpw(password.encode("utf-8"), salt).decode("utf-8"),
        role="user",
        is_active=True,
        created_at=now,
        updated_at=now,
    )
    db.users.insert_one(
        {
            "_id": user.id,
            "name": user.name,
            "email": user.email,
            "password_salt": user.password_salt,
            "password_hash": user.password_hash,
            "role": user.role,
            "is_active": user.is_active,
            "created_at": user.created_at,
            "updated_at": user.updated_at,
            "last_login_at": user.last_login_at,
        }
    )
    return user


def get_user_by_email(db: Database, email: str) -> User | None:
    return _to_user(db.users.find_one({"email": email}))


def get_user_by_id(db: Database, user_id: int) -> User | None:
    return _to_user(db.users.find_one({"_id": user_id}))


def update_last_login(db: Database, user_id: int, when: datetime) -> None:
    db.users.update_one(
        {"_id": user_id},
        {"$set": {"last_login_at": when, "updated_at": when}},
    )


def verify_password(user: User, password: str) -> bool:
    return bcrypt.checkpw(password.encode("utf-8"), user.password_hash.encode("utf-8"))
