from fastapi import FastAPI

import backend.models as models
from backend.database import engine
# Import routers
from backend.routers.distributions import router as distributions_router
from backend.routers.playsets import router as playsets_router
from backend.routers.servers import router as servers_router

app = FastAPI()
app.include_router(distributions_router, prefix="/distributions")
app.include_router(playsets_router, prefix="/playsets")
app.include_router(servers_router, prefix="/servers")


@app.on_event("startup")
async def startup():
    await models.create_tables(engine)
