from sqlalchemy import ForeignKey, Table, Column, Enum, Text, String

from typing import List, Dict
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.ext.mutable import MutableDict
from sqlalchemy import JSON, select
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


machine_project = Table(
    "machine_project",
    db.Model.metadata,
    Column("machines", ForeignKey("machines.id"), primary_key=True),
    Column("projects", ForeignKey("projects.id"), primary_key=True)
)

class Machine(db.Model):
    __tablename__ = "machines"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    address: Mapped[str] = mapped_column()

    os_type: Mapped[str] = mapped_column()
    
    os: Mapped[str] = mapped_column()

    user: Mapped[str] = mapped_column()

    cpu: Mapped[str] = mapped_column()

    port: Mapped[int] = mapped_column()

    model: Mapped[str] = mapped_column()

    manufacturer: Mapped[str] = mapped_column()

    is_online: Mapped[bool] = mapped_column(default=False)

    projects: Mapped[List["Project"]] = relationship(secondary=machine_project, back_populates="machines")


    def __repr__(self):
        return f"{self.user} running {self.os} address: {self.address}"


class Watchlist(db.Model):
    __tablename__ = "watchlist"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column()

class Project(db.Model):
    __tablename__ = "projects"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True)
    strategy_type: Mapped[str] = mapped_column()

    config: Mapped[Dict] = mapped_column(MutableDict.as_mutable(JSON), default=dict)

    deployment_metadata: Mapped[Dict] = mapped_column(MutableDict.as_mutable(JSON), default=dict)
    
    machines: Mapped[List["Machine"]] = relationship(secondary=machine_project, back_populates="projects")

    @staticmethod
    def hydrate_machines(machines):
        machine_ids = [m['id'] for m in machines]
        machine_objects = {m.id: m for m in db.session.execute(select(Machine).where(Machine.id.in_(machine_ids))).scalars().all()}
        updated_machines = []

        for machine_metadata in machines:
            idk = machine_metadata.copy()
            idk['machine_object'] = machine_objects[machine_metadata['id']]
            updated_machines.append(idk)
        return updated_machines

    def __repr__(self):
        return f"Project:{self.name} using the strategy {self.strategy_type}"
    

