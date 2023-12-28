from fastapi import FastAPI

import backend.models as models
from backend.database import engine
from backend.routers.distributions import router as distributions_router

app = FastAPI()
app.include_router(distributions_router, prefix="/distributions")


@app.on_event("startup")
async def startup():
    await models.create_tables(engine)


@app.get("/")
async def hello_world():
    return "Hello, world!"
