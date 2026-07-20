from typing import Dict, List, Optional
from sqlalchemy import JSON, Column
from sqlalchemy.ext.mutable import MutableDict
from sqlmodel import Field, Relationship, SQLModel

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

    containers: List["Container"] = Relationship(back_populates="machine")

    def __repr__(self):
        return f"{self.user} running {self.os} address: {self.address}"

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

    machine_id: int = Field(foreign_key="machines.id")
    stack_id: Optional[int] = Field(default=None, foreign_key="container_stacks.id")

    machine: Optional[Machine] = Relationship(back_populates="containers")
    stack: Optional[ContainerStack] = Relationship(back_populates="containers")

    def __repr__(self):
        return f"Project:{self.name} using image: {self.image}"
    

class Blueprint(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(unique=True)
    default_image: str
    config: Dict = Field(
        default_factory=dict,
        sa_column=Column(MutableDict.as_mutable(JSON), default=dict)
    )