from typing import Dict, List, Optional
from sqlalchemy import Column, JSON, DateTime, func
from sqlalchemy.ext.mutable import MutableDict
from sqlmodel import Field, Relationship, SQLModel
from datetime import datetime
class ContainerConfigBase(SQLModel):
    description: Optional[str] = Field(default=None)
    name: str = Field(unique=True)
    spec: Dict = Field(
        default_factory=dict,
        sa_column=Column(MutableDict.as_mutable(JSON), default=dict)
    ) 


class ContainerConfig(ContainerConfigBase, table=True):
    __tablename__ = "container_configs"

    id: Optional[int] = Field(default=None, primary_key=True)
        
    created_at: Optional[datetime] = Field(
        default=None, 
        sa_column=Column(DateTime(timezone=True), server_default=func.now())
    )
    updated_at: Optional[datetime] = Field(
        default=None, 
        sa_column=Column(DateTime(timezone=True), onupdate=func.now(), server_default=func.now())
    )

    def __repr__(self):
        return f"<ContainerConfig(name={self.name})>"
    