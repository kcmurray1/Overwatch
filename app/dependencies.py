from sqlmodel import Session, create_engine
import os

DATABASE_URL="sqlite:///./instance/machines.db"


engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

def get_session():
    with Session(engine) as session:
        yield session