from typing import List, Optional
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

    containers: List["Container"] = Relationship(back_populates="machine", cascade_delete=True)

    def __repr__(self):
        return f"{self.user} running {self.os} address: {self.address}"