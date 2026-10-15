from core.database import client, database


def create_indexes() -> None:
    client.admin.command("ping")
    database.users.create_index("email", unique=True)
    database.sessions.create_index("session_token", unique=True)
    database.sessions.create_index("user_id")
    database.blogs.create_index("user_id")
