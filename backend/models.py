from typing import List

from pydantic import BaseModel
from sqlalchemy import Column, String, Integer, Boolean, Table, ForeignKey
from sqlalchemy.ext.asyncio import AsyncEngine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


async def create_tables(engine: AsyncEngine):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


# Association table for many-to-many relationship
mod_playset_association = Table(
    "mod_playset",
    Base.metadata,
    Column("mod_id", String, ForeignKey("mod.id"), primary_key=True),
    Column("playset_id", String, ForeignKey("playset.id"), primary_key=True),
)


class Server(Base):
    __tablename__ = "server"
    id = Column(String, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)  # EX: "My Paper Server"
    loader = Column(String, index=True, nullable=False)  # EX: "paper"
    game_version = Column(String, index=True, nullable=False)  # EX: "1.16.5"
    server_mods = relationship("ServerMod", back_populates="server")
    port = Column(Integer, default=25565)
    eula = Column(Boolean, default=True)
    allocated_memory = Column(Integer, default=2048)
    enable_jmx_monitoring = Column(Boolean, default=False)
    rcon_port = Column(Integer, default=25575)
    level_seed = Column(String)
    gamemode = Column(String, default="survival")
    enable_command_block = Column(Boolean, default=False)
    enable_query = Column(Boolean, default=False)
    enforce_secure_profile = Column(Boolean, default=True)
    level_name = Column(String, default="world")
    motd = Column(String, default="A Fourdrinier Server")
    query_port = Column(Integer, default=25565)
    pvp = Column(Boolean, default=True)
    generate_structures = Column(Boolean, default=True)
    max_chained_neighbor_updates = Column(Integer, default=1000000)
    difficulty = Column(String, default="hard")
    network_compression_threshold = Column(Integer, default=256)
    max_tick_time = Column(Integer, default=60000)
    require_resource_pack = Column(Boolean, default=False)
    use_native_transport = Column(Boolean, default=True)
    max_players = Column(Integer, default=20)
    online_mode = Column(Boolean, default=True)
    enable_status = Column(Boolean, default=True)
    allow_flight = Column(Boolean, default=False)
    initial_disabled_packs = Column(String)
    broadcast_rcon_to_ops = Column(Boolean, default=True)
    view_distance = Column(Integer, default=32)
    resource_pack_prompt = Column(String)
    allow_nether = Column(Boolean, default=True)
    enable_rcon = Column(Boolean, default=False)
    sync_chunk_writes = Column(Boolean, default=True)
    op_permission_level = Column(Integer, default=4)
    prevent_proxy_connections = Column(Boolean, default=False)
    hide_online_players = Column(Boolean, default=False)
    resource_pack = Column(String)
    entity_broadcast_range_percentage = Column(Integer, default=100)
    simulation_distance = Column(Integer, default=12)
    rcon_password = Column(String)
    player_idle_timeout = Column(Integer, default=0)
    force_gamemode = Column(Boolean, default=False)
    rate_limit = Column(Integer, default=0)
    hardcore = Column(Boolean, default=False)
    whitelisted = Column(Boolean, default=False)
    broadcast_console_to_ops = Column(Boolean, default=True)
    spawn_npcs = Column(Boolean, default=True)
    spawn_animals = Column(Boolean, default=True)
    function_permission_level = Column(Integer, default=2)
    text_filtering_config = Column(String)
    spawn_monsters = Column(Boolean, default=True)
    enforce_whitelist = Column(Boolean, default=False)
    spawn_protection = Column(Integer, default=16)
    resource_pack_sha1 = Column(String)
    max_world_size = Column(Integer, default=29999984)
    ops = Column(String, default='{"ops": ["FortuityYT"]}')


class Playset(Base):
    __tablename__ = "playset"
    id = Column(String, primary_key=True, index=True)
    name = Column(String, nullable=False)
    mods = relationship(
        "Mod", secondary=mod_playset_association, back_populates="playsets"
    )


class Mod(Base):
    __tablename__ = "mod"
    id = Column(String, primary_key=True)
    title = Column(String)
    playsets = relationship(
        "Playset", secondary=mod_playset_association, back_populates="mods"
    )


class ServerMod(Base):
    __tablename__ = "server_mod"
    id = Column(String, primary_key=True)
    title = Column(String)
    project_id = Column(String)
    version_id = Column(String)
    version_name = Column(String)
    supported_versions = Column(String)
    url = Column(String)
    role = Column(String)
    server_id = Column(String, ForeignKey("server.id"))
    server = relationship("Server", back_populates="server_mods")


# Pydantic model for returning a playset with the list of all mods associated with it
class PlaysetResponse(BaseModel):
    id: str
    name: str
    mods: List[str]  # List of mod IDs


class ServerModResponse(BaseModel):
    id: str
    title: str
    version: str
    version_name: str
    role: str


class ServerResponse(BaseModel):
    id: str
    name: str
    game_version: str
    loader: str
    projects: List[ServerModResponse]
