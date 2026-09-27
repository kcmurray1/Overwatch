from typing import Dict, List, Optional
from sqlalchemy import Column, JSON
from sqlalchemy.ext.mutable import MutableDict, MutableList
from sqlmodel import Field, Relationship, SQLModel

class ContainerBase(SQLModel):
    id: Optional[int] = Field(default=None, primary_key=True)
    docker_id: Optional[str] = Field(default=None, unique=True)
    image: str
    name: str = Field(unique=True)
    config: Dict = Field(
        default_factory=dict,
        sa_column=Column(MutableDict.as_mutable(JSON), default=dict)
    )
    state: str


class ContainerStack(SQLModel, table=True):
    __tablename__ = "container_stacks"

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(unique=True)

    containers: List["Container"] = Relationship(back_populates="stack")


class Container(ContainerBase, table=True):
    __tablename__ = "containers"

    machine_id: int = Field(foreign_key="machines.id", ondelete="CASCADE")
    stack_id: Optional[int] = Field(default=None, foreign_key="container_stacks.id")

    machine: Optional["Machine"] = Relationship(back_populates="containers")
    stack: Optional[ContainerStack] = Relationship(back_populates="containers")
    status: str = Field(default="offline", nullable=False)

    def __repr__(self):
        return f"Project:{self.name} using image: {self.image}"
    