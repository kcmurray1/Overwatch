from sqlalchemy import ForeignKey, Table, Column, Enum, Text, String

from typing import List
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.ext.mutable import MutableDict
from sqlalchemy import JSON
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()



class Machine(db.Model):
    __tablename__ = "machines"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    address: Mapped[str] = mapped_column()

    #NOTE: convert to enumerator
    os_type: Mapped[str] = mapped_column()
    
    os: Mapped[str] = mapped_column()

    user: Mapped[str] = mapped_column()

    cpu: Mapped[str] = mapped_column()

    port: Mapped[int] = mapped_column()

    model: Mapped[str] = mapped_column()

    manufacturer: Mapped[str] = mapped_column()

    is_online: Mapped[bool] = mapped_column(default=False)

    deployments: Mapped[List["MachineProject"]] = relationship(back_populates="machine", cascade="all, delete-orphan")


    def __repr__(self):
        return f"{self.user} running {self.os} address: {self.address}"


class Watchlist(db.Model):
    __tablename__ = "watchlist"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column()

class Project(db.Model):
    __tablename__ = "project"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column()
    strategy_type: Mapped[str] = mapped_column()
    compose_text: Mapped[str] = mapped_column(Text)
    config: Mapped[MutableDict[JSON]] = mapped_column

    deployments: Mapped[List["MachineProject"]] = relationship(back_populates="project", cascade="all, delete-orphan")

class MachineProject(db.Model):
    __tablename__ = "machine_projects"
    id: Mapped[int] = mapped_column(primary_key=True)
    machine_id: Mapped[int] = mapped_column(ForeignKey("machines.id"))
    project_id: Mapped[int] = mapped_column(ForeignKey("project.id"))
    
    # Relationships
    machine: Mapped["Machine"] = db.relationship(back_populates="deployments")
    project: Mapped["Project"] = db.relationship(back_populates="deployments")

    # Your metadata
    container_id: Mapped[str] = mapped_column(nullable=True)
    status: Mapped[str] = mapped_column(default="stopped")