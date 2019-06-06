import uuid

import sqlalchemy

from app.database import Base


class Note(Base):
    id = sqlalchemy.Column(sqlalchemy.String,
                           primary_key=True,
                           default=lambda: uuid.uuid4().hex.lower())
    title = sqlalchemy.Column(sqlalchemy.Text)
    body = sqlalchemy.Column(sqlalchemy.Text)

    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'title': self.title,
            'body': self.body,
        }
