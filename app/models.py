from sqlalchemy import ForeignKey, Table, Column, Enum, Text, String

from typing import List, Optional

from sqlalchemy.orm import Mapped, mapped_column

from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


class Machine(db.Model):
    __tablename__ = "machines"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    # name: Mapped[str] = mapped_column()

    addr: Mapped[str] = mapped_column(String(18))

    # os_type: Mapped[str] = mapped_column()

    user: Mapped[str] = mapped_column()

    port: Mapped[int] = mapped_column()


class Watchlist(db.Model):
    __tablename__ = "watchlist"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column()