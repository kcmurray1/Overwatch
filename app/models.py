from sqlalchemy import ForeignKey, Table, Column, Enum, Text, String


from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.ext.mutable import MutableDict
from sqlalchemy import JSON
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


class Machine(db.Model):
    __tablename__ = "machines"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    # name: Mapped[str] = mapped_column()

    address: Mapped[str] = mapped_column()

    #NOTE: convert to enumerator
    os_type: Mapped[str] = mapped_column()
    
    os: Mapped[str] = mapped_column()

    user: Mapped[str] = mapped_column()

    cpu: Mapped[str] = mapped_column()

    port: Mapped[int] = mapped_column()

    model: Mapped[str] = mapped_column()

    manufacturer: Mapped[str] = mapped_column()


    def __repr__(self):
        return f"{self.user} running {self.os} address: {self.address}"


class Watchlist(db.Model):
    __tablename__ = "watchlist"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column()