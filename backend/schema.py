from typing import List, Any, Optional

from pydantic import BaseModel, Field


class PlaysetCreateSchema(BaseModel):
    name: str = "My Playset"  # Default name if not otherwise defined
    mods: List[Any] = []  # Default to an empty list


class ModSchema(BaseModel):
    mod_id: str


class AddModsToPlaysetSchema(BaseModel):
    mods: List[ModSchema]


class AddCollectionToPlaysetSchema(BaseModel):
    collection_id: str


class RenamePlaysetSchema(BaseModel):
    name: str


class ServerCreateSchema(BaseModel):
    name: str = Field(default="My Server", example="Vanilla+ Server")
    loader: str = Field(..., pattern="^(paper|fabric)$", example="paper")
    game_version: str = Field(..., pattern=r"^\d+\.\d+\.\d+$", example="1.16.5")


class AddPlaysetToServerSchema(BaseModel):
    playset_id: str = Field(..., pattern=r"^[a-zA-Z0-9]{8}$", example="abcd1234")


class UpdateServerSettingsSchema(BaseModel):
    example: Optional[str] = Field(None)
    name: Optional[str] = Field(None)
    loader: Optional[str] = Field(None)
    game_version: Optional[str] = Field(None)
    port: Optional[int] = Field(None)
    eula: Optional[bool] = Field(None)
    allocated_memory: Optional[int] = Field(None)
    enable_jmx_monitoring: Optional[bool] = Field(None)
    rcon_port: Optional[int] = Field(None)
    level_seed: Optional[str] = Field(None)
    gamemode: Optional[str] = Field(None)
    enable_command_block: Optional[bool] = Field(None)
    enable_query: Optional[bool] = Field(None)
    enforce_secure_profile: Optional[bool] = Field(None)
    level_name: Optional[str] = Field(None)
    motd: Optional[str] = Field(None)
    query_port: Optional[int] = Field(None)
    pvp: Optional[bool] = Field(None)
    generate_structures: Optional[bool] = Field(None)
    max_chained_neighbor_updates: Optional[int] = Field(None)
    difficulty: Optional[str] = Field(None)
    network_compression_threshold: Optional[int] = Field(None)
    max_tick_time: Optional[int] = Field(None)
    require_resource_pack: Optional[bool] = Field(None)
    use_native_transport: Optional[bool] = Field(None)
    max_players: Optional[int] = Field(None)
    online_mode: Optional[bool] = Field(None)
    enable_status: Optional[bool] = Field(None)
    allow_flight: Optional[bool] = Field(None)
    initial_disabled_packs: Optional[str] = Field(None)
    broadcast_rcon_to_ops: Optional[bool] = Field(None)
    view_distance: Optional[int] = Field(None)
    resource_pack_prompt: Optional[str] = Field(None)
    allow_nether: Optional[bool] = Field(None)
    enable_rcon: Optional[bool] = Field(None)
    sync_chunk_writes: Optional[bool] = Field(None)
    op_permission_level: Optional[int] = Field(None)
    prevent_proxy_connections: Optional[bool] = Field(None)
    hide_online_players: Optional[bool] = Field(None)
    resource_pack: Optional[str] = Field(None)
    entity_broadcast_range_percentage: Optional[int] = Field(None)
    simulation_distance: Optional[int] = Field(None)
    rcon_password: Optional[str] = Field(None)
    player_idle_timeout: Optional[int] = Field(None)
    force_gamemode: Optional[bool] = Field(None)
    rate_limit: Optional[int] = Field(None)
    hardcore: Optional[bool] = Field(None)
    whitelisted: Optional[bool] = Field(None)
    broadcast_console_to_ops: Optional[bool] = Field(None)
    spawn_npcs: Optional[bool] = Field(None)
    spawn_animals: Optional[bool] = Field(None)
    function_permission_level: Optional[int] = Field(None)
    text_filtering_config: Optional[str] = Field(None)
    spawn_monsters: Optional[bool] = Field(None)
    enforce_whitelist: Optional[bool] = Field(None)
    spawn_protection: Optional[int] = Field(None)
    resource_pack_sha1: Optional[str] = Field(None)
    max_world_size: Optional[int] = Field(None)
    ops: Optional[List[str]] = None
