from sqlmodel import SQLModel, Field, Relationship
from sqlalchemy import Column, JSON, ForeignKey, Table
from sqlalchemy.ext.mutable import MutableDict, MutableList
# from sqlalchemy import select
from typing import List, Dict, Optional
from sqlmodel import Session, select, delete
# Standard SQLAlchemy Link Table for Many-to-Many
machine_project = Table(
    "machine_project",
    SQLModel.metadata,
    Column("machines", ForeignKey("machines.id"), primary_key=True),
    Column("projects", ForeignKey("projects.id"), primary_key=True)
)

class MachineBase(SQLModel):
    address: str
    user: str
    port: int

class Machine(MachineBase, table=True):
    __tablename__ = "machines"

    id: Optional[int] = Field(default=None, primary_key=True)
    address: str
    os_type: str
    os: str
    user: str
    cpu: str
    port: int
    model: str
    manufacturer: str
    is_online: bool = Field(default=False)
    tailscale_ip: Optional[str] = Field(default=None)

    # Many-to-Many Relationship link using your secondary table
    projects: List["Project"] = Relationship(
        back_populates="machines", 
        sa_relationship_kwargs={"secondary": machine_project}
    )

    def __repr__(self):
        return f"{self.user} running {self.os} address: {self.address}"


class Watchlist(SQLModel, table=True):
    __tablename__ = "watchlist"

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str


class Project(SQLModel, table=True):
    __tablename__ = "projects"

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(unique=True)
    strategy_type: str
    is_running: bool = Field(default=False)

    # Use standard SQLAlchemy sa_column overrides to keep your JSON mutable tracking intact
    config: Dict = Field(
        default_factory=dict,
        sa_column=Column(MutableDict.as_mutable(JSON), default=dict)
    )
    deployment_metadata: List = Field(
        default_factory=list,
        sa_column=Column(MutableList.as_mutable(JSON), default=list)
    )

    machines: List["Machine"] = Relationship(
        back_populates="projects", 
        sa_relationship_kwargs={"secondary": machine_project}
    )

    @staticmethod
    def hydrate_machines(session: Session, machines: list):
        """Return a list of Machine database models given a list of Machine table id's"""

        machine_ids = [m['id'] for m in machines]
        print(machine_ids)
        # SQLModel session.exec allows executing standard SQLAlchemy statements
        machine_objects = {
            m.id: m for m in session.exec(
                select(Machine).where(Machine.id.in_(machine_ids))
            ).all()
        }
        
        updated_machines = []
        for machine_metadata in machines:
            print(machine_metadata)
            machine_copy = machine_metadata.copy()
            machine_copy['machine_object'] = machine_objects[machine_metadata['id']]
            updated_machines.append(machine_copy)
        return updated_machines

    def __repr__(self):
        return f"Project:{self.name} using the strategy {self.strategy_type}"