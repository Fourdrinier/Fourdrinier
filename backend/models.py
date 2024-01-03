from sqlalchemy import Column, String, JSON, Table, ForeignKey
from sqlalchemy.ext.asyncio import AsyncEngine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

from pydantic import BaseModel
from typing import List

Base = declarative_base()


async def create_tables(engine: AsyncEngine):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

# Association table for many-to-many relationship
mod_playset_association = Table(
    'mod_playset', Base.metadata,
    Column('mod_id', String, ForeignKey('mod.id'), primary_key=True),
    Column('playset_id', String, ForeignKey('playset.id'), primary_key=True)
)


class Server(Base):
    __tablename__ = "server"
    id = Column(String, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)  # EX: "My Paper Server"
    distribution = Column(String, index=True, nullable=False)  # EX: "paper"
    mc_version = Column(String, index=True, nullable=False)  # EX: "1.16.5"


class Playset(Base):
    __tablename__ = "playset"
    id = Column(String, primary_key=True, index=True)
    name = Column(String, nullable=False)
    mods = relationship("Mod", secondary=mod_playset_association, back_populates="playsets")


class Mod(Base):
    __tablename__ = 'mod'
    id = Column(String, primary_key=True)
    title = Column(String, unique=True)
    playsets = relationship("Playset", secondary=mod_playset_association, back_populates="mods")


# Pydantic model for returning a playset with the list of all mods associated with it
class PlaysetResponse(BaseModel):
    id: str
    name: str
    mods: List[str]  # List of mod IDs
