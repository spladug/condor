from sqlalchemy import Column, Unicode, UnicodeText, Integer, ForeignKey, Enum, String, engine_from_config
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.orm.exc import NoResultFound


POLL_STATES = [
    "setup",
    "nominations",
    "voting",
    "closed",
]


Base = declarative_base()


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    email_address = Column(Unicode(254), unique=True)

    @classmethod
    def _by_email_address(cls, db, email_address):
        return (db.query(cls)
                  .filter_by(email_address=email_address)
                  .one())

    @classmethod
    def by_email(cls, db, email_address):
        try:
            user = cls._by_email_address(db, email_address)
        except NoResultFound:
            db.rollback()

            try:
                user = User(email_address=email_address)
                db.add(user)
                db.commit()
            except IntegrityError:
                db.rollback()
                user = cls._by_email_address(email_address)
        return User(id=user.id, email_address=user.email_address)


class Poll(Base):
    __tablename__ = "poll"

    id = Column(Integer, primary_key=True)
    state = Column(Enum(*POLL_STATES), nullable=False, default="setup")
    creator_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    title = Column(Unicode(80), nullable=False)
    description = Column(UnicodeText)

    creator = relationship("User")


class Choice(Base):
    __tablename__ = "choice"

    poll_id = Column(Integer, ForeignKey("poll.id"), primary_key=True)
    id = Column(String(20), primary_key=True)
    description = Column(Unicode(100), nullable=False)


class Ballot(Base):
    __tablename__ = "ballot"

    user_id = Column(Integer, ForeignKey("user.id"), primary_key=True)
    poll_id = Column(Integer, ForeignKey("poll.id"), primary_key=True)
    # TODO: the content of the vote


class Invite(Base):
    __tablename__ = "invite"


def create_schema(app_config):
    engine = engine_from_config(app_config, prefix="database.")
    Base.metadata.create_all(bind=engine)


if __name__ == "__main__":
    create_schema()
