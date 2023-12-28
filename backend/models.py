from sqlalchemy import Column, String
from sqlalchemy.ext.asyncio import AsyncEngine
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


async def create_tables(engine: AsyncEngine):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


class Server(Base):
    __tablename__ = "servers"
    id = Column(String, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)  # EX: "My Paper Server"
    distribution = Column(String, index=True, nullable=False)  # EX: "paper"
    mc_version = Column(String, index=True, nullable=False)  # EX: "1.16.5"
    build_version = Column(String, index=True, nullable=False)  # EX: "652"
