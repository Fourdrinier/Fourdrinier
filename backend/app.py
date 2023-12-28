from fastapi import FastAPI

from backend.routers.distributions import router as distributions_router

app = FastAPI()
app.include_router(distributions_router, prefix="/distributions")


@app.get("/")
async def hello_world():
    return "Hello, world!"
