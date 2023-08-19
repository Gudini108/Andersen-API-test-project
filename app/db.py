"""Database engine and base models"""

import ormar
import databases
import sqlalchemy

from .config import settings


database = databases.Database(settings.db_url)
metadata = sqlalchemy.MetaData()


class BaseMeta(ormar.ModelMeta):
    metadata = metadata
    database = database


class TodoUser(ormar.Model):
    """Basic User model"""
    class Meta(BaseMeta):
        tablename = "users"

    id: int = ormar.Integer(primary_key=True)
    first_name: str = ormar.String(max_length=128, nullable=False)
    last_name: str = ormar.Text(nullable=True)
    username: str = ormar.String(max_length=128, unique=True, nullable=False)
    password: str = ormar.String(min_length=6, max_length=128, nullable=False)


class TodoTask(ormar.Model):
    """Model for Tasks"""
    class Meta(BaseMeta):
        tablename = "tasks"

    id: int = ormar.Integer(primary_key=True)
    title: str = ormar.String(max_length=255, nullable=False)
    description: str = ormar.Text(nullable=True)
    status: str = ormar.String(max_length=20, default="New", nullable=True,
                               choices=["New", "In Progress", "Completed"])
    user: TodoUser = ormar.ForeignKey(TodoUser, related_name="tasks",
                                      ondelete="CASCADE", nullable=False)


engine = sqlalchemy.create_engine(settings.db_url)
metadata.create_all(engine)
