from datetime import datetime

from pymongo import ReturnDocument
from pymongo.database import Database

from core.database import get_next_id
from models.blog import Blog


def _to_blog(document: dict) -> Blog:
    return Blog(
        id=document["_id"],
        title=document["title"],
        content=document["content"],
        keywords=document["keywords"],
        created_at=document["created_at"],
        user_id=document.get("user_id"),
    )


def create_blog(
    db: Database, *, user_id: int, title: str, content: str, keywords: str
) -> Blog:
    blog = Blog(
        id=get_next_id(db, "blogs"),
        title=title,
        content=content,
        keywords=keywords,
        created_at=datetime.utcnow(),
        user_id=user_id,
    )
    db.blogs.insert_one(
        {
            "_id": blog.id,
            "title": blog.title,
            "content": blog.content,
            "keywords": blog.keywords,
            "created_at": blog.created_at,
            "user_id": blog.user_id,
        }
    )
    return blog


def get_blogs(db: Database) -> list[Blog]:
    return [
        _to_blog(document)
        for document in db.blogs.find().sort("created_at", -1)
    ]


def get_blog(db: Database, blog_id: int) -> Blog | None:
    document = db.blogs.find_one({"_id": blog_id})
    return _to_blog(document) if document else None


def get_my_blogs(db: Database, *, user_id: int) -> list[Blog]:
    return [
        _to_blog(document)
        for document in db.blogs.find({"user_id": user_id}).sort("created_at", -1)
    ]


def get_my_blog(db: Database, *, user_id: int, blog_id: int) -> Blog | None:
    document = db.blogs.find_one({"_id": blog_id, "user_id": user_id})
    return _to_blog(document) if document else None


def update_blog(
    db: Database,
    *,
    user_id: int,
    blog_id: int,
    title: str,
    content: str,
    keywords: str,
) -> Blog | None:
    document = db.blogs.find_one_and_update(
        {"_id": blog_id, "user_id": user_id},
        {"$set": {"title": title, "content": content, "keywords": keywords}},
        return_document=ReturnDocument.AFTER,
    )
    return _to_blog(document) if document else None


def delete_blog(db: Database, *, user_id: int, blog_id: int) -> bool:
    result = db.blogs.delete_one({"_id": blog_id, "user_id": user_id})
    return result.deleted_count == 1
