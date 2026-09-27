from sqlmodel import Session, create_engine
from sqlalchemy import event
import os

DATABASE_URL="sqlite:///./instance/machines.db"


engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})


@event.listens_for(engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()


def get_session():
    with Session(engine) as session:
        yield session