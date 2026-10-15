from pathlib import Path
import os

from dotenv import load_dotenv
from pymongo import MongoClient, ReturnDocument
from pymongo.database import Database

load_dotenv(Path(__file__).resolve().parents[1] / ".env")

MONGODB_URI = os.getenv("MONGODB_URI", "mongodb://localhost:27017")
MONGODB_DATABASE = os.getenv("MONGODB_DATABASE", "ai_blog_agent")

client = MongoClient(MONGODB_URI, serverSelectionTimeoutMS=5000)
database: Database = client[MONGODB_DATABASE]


def get_next_id(db: Database, sequence_name: str) -> int:
    counter = db.counters.find_one_and_update(
        {"_id": sequence_name},
        {"$inc": {"value": 1}},
        upsert=True,
        return_document=ReturnDocument.AFTER,
    )
    return int(counter["value"])
