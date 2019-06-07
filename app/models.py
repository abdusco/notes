import uuid
from datetime import datetime

import sqlalchemy

from app.database import Base


class Note(Base):
    id = sqlalchemy.Column(sqlalchemy.String,
                           primary_key=True,
                           default=lambda: uuid.uuid4().hex.lower())
    body = sqlalchemy.Column(sqlalchemy.Text)
    last_accessed = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.now)

    def touch(self) -> None:
        self.last_accessed = datetime.now()

    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'body': self.body,
            'last_accessed': self.last_accessed,
        }
