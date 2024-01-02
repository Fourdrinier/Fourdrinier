from sqlalchemy import Table, Column, String, JSON, ForeignKey
from sqlalchemy.ext.asyncio import AsyncEngine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


async def create_tables(engine: AsyncEngine):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


# Association table for the many-to-many relationship
mod_playset_association = Table(
    "mod_playset",
    Base.metadata,
    Column("mod_id", String, ForeignKey("mods.id")),
    Column("playset_id", String, ForeignKey("playsets.id")),
)


class Server(Base):
    __tablename__ = "servers"
    id = Column(String, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)  # EX: "My Paper Server"
    distribution = Column(String, index=True, nullable=False)  # EX: "paper"
    mc_version = Column(String, index=True, nullable=False)  # EX: "1.16.5"
    build_version = Column(String, index=True, nullable=False)  # EX: "652"


class Mod(Base):
    __tablename__ = "mods"
    id = Column(String, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)  # EX: "EssentialsX"
    loader = Column(String, index=True, nullable=False)  # EX: "paper"
    supported_versions = Column(JSON, nullable=False)  # EX: ["1.12.4", "1.19.2"]
    versions = relationship("Version", back_populates="mod")
    playsets = relationship(
        "Playset", secondary=mod_playset_association, back_populates="mods"
    )


class Version(Base):
    __tablename__ = "versions"
    id = Column(String, primary_key=True, index=True)
    version_number = Column(String, nullable=False)
    game_version = Column(String, nullable=False)  # Added this field
    dependencies = Column(
        JSON, nullable=False
    )  # EX: [{ mod_id: "9s6osm5g", dependency_type: "optional", required_version: "hFdJG9fY"}]
    mod_id = Column(String, ForeignKey("mods.id"))
    mod = relationship("Mod", back_populates="versions")


class Playset(Base):
    __tablename__ = "playsets"
    id = Column(String, primary_key=True, index=True)
    name = Column(String, nullable=False)
    mods = relationship(
        "Mod", secondary=mod_playset_association, back_populates="playsets"
    )
