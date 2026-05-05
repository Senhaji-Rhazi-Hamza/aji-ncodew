from sqlalchemy import create_engine, String, Integer, ForeignKey, select
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
    relationship,
    Session,
    object_session,
)
from datetime import datetime


# Base class
class Base(DeclarativeBase):

    @classmethod
    def get(cls, session: Session, id):
        return session.get(cls, id)

    @classmethod
    def all(cls, session: Session):
        return session.execute(select(cls)).scalars().all()

    @classmethod
    def create(cls, session: Session, **kwargs):
        instance = cls(**kwargs)
        session.add(instance)
        session.commit()
        session.refresh(instance)
        return instance

    def update(self, **kwargs):
        session = object_session(self)
        for key, value in kwargs.items():
            setattr(self, key, value)
        if session is not None:
            session.add(self)
            session.commit()
        return self

    def delete(self, **kwargs):
        session = object_session(self)
        if session is not None:
            session.delete(self)
            session.commit()
        else:
            raise Exception(f"no session attached to instance {self}")
        return self

    def to_dict(self):
        return {col.name: getattr(self, col.name) for col in self.__table__.columns}

    def __repr__(self):
        cols = ", ".join(
            f"{col.name}={getattr(self, col.name)!r}" for col in self.__table__.columns
        )
        return f"<{self.__class__.__name__}({cols})>"
