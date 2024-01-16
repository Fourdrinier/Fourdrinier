from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, Field, conint


# Allowed values for gamemode
class GameMode(Enum):
    SURVIVAL = "survival"
    CREATIVE = "creative"
    ADVENTURE = "adventure"
    SPECTATOR = "spectator"


# Allowed values for loader
class Loader(Enum):
    FABRIC = "fabric"


# Allowed values for game version
class GameVersion(Enum):
    GAME_VERSION = "1.20.1"


# Allowed values for difficulty
class Difficulty(Enum):
    PEACEFUL = "peaceful"
    EASY = "easy"
    NORMAL = "normal"
    HARD = "hard"


class UpdateServerSettingsSchema(BaseModel):
    name: Optional[str] = Field(None)
    loader: Optional[Loader] = Field(None)
    game_version: Optional[GameVersion] = Field(None)
    port: Optional[conint(gt=1023, lt=49152)] = Field(None)
    eula: Optional[bool] = Field(None)
    allocated_memory: Optional[conint(ge=1024)] = Field(None)
    enable_jmx_monitoring: Optional[bool] = Field(None)
    rcon_port: Optional[conint(gt=1023, lt=49152)] = Field(None)
    level_seed: Optional[str] = Field(None)
    gamemode: Optional[GameMode] = Field(None)
    enable_command_block: Optional[bool] = Field(None)
    enable_query: Optional[bool] = Field(None)
    enforce_secure_profile: Optional[bool] = Field(None)
    level_name: Optional[str] = Field(None)  # Add validator later
    motd: Optional[str] = Field(None)  # Add validator later
    query_port: Optional[conint(gt=1023, lt=49152)] = Field(None)
    pvp: Optional[bool] = Field(None)
    generate_structures: Optional[bool] = Field(None)
    max_chained_neighbor_updates: Optional[conint(ge=512)] = Field(None)
    difficulty: Optional[Difficulty] = Field(None)
    network_compression_threshold: Optional[conint(ge=-1)] = Field(None)
    max_tick_time: Optional[conint(ge=-1)] = Field(None)
    # require_resource_pack: Optional[bool] = Field(None)  -   Add this later
    use_native_transport: Optional[bool] = Field(None)
    max_players: Optional[conint(ge=1)] = Field(None)
    online_mode: Optional[bool] = Field(None)
    enable_status: Optional[bool] = Field(None)
    allow_flight: Optional[bool] = Field(None)
    # initial_disabled_packs: Optional[str] = Field(None)  -  Add this laterwhat i
    broadcast_rcon_to_ops: Optional[bool] = Field(None)
    view_distance: Optional[conint(ge=1)] = Field(None)
    # resource_pack_prompt: Optional[str] = Field(None)  -  Add this later
    allow_nether: Optional[bool] = Field(None)
    enable_rcon: Optional[bool] = Field(None)
    sync_chunk_writes: Optional[bool] = Field(None)
    op_permission_level: Optional[conint(ge=1, le=4)] = Field(None)
    prevent_proxy_connections: Optional[bool] = Field(None)
    hide_online_players: Optional[bool] = Field(None)
    # resource_pack: Optional[str] = Field(None)  -  Add this later
    entity_broadcast_range_percentage: Optional[conint(ge=0, le=100)] = Field(None)
    simulation_distance: Optional[conint(ge=1)] = Field(None)
    rcon_password: Optional[str] = Field(None)
    player_idle_timeout: Optional[conint(ge=0)] = Field(None)
    force_gamemode: Optional[bool] = Field(None)
    rate_limit: Optional[conint(ge=0)] = Field(None)
    hardcore: Optional[bool] = Field(None)
    whitelisted: Optional[bool] = Field(None)
    broadcast_console_to_ops: Optional[bool] = Field(None)
    spawn_npcs: Optional[bool] = Field(None)
    spawn_animals: Optional[bool] = Field(None)
    function_permission_level: Optional[conint(ge=1, le=4)] = Field(None)
    # text_filtering_config: Optional[str] = Field(None)  -  Add this later
    spawn_monsters: Optional[bool] = Field(None)
    enforce_whitelist: Optional[bool] = Field(None)
    spawn_protection: Optional[conint(ge=0)] = Field(None)
    # resource_pack_sha1: Optional[str] = Field(None)  -  Add this later
    max_world_size: Optional[conint(ge=1024, le=2147483647)] = Field(None)
    ops: Optional[List[str]] = None
