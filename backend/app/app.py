from fastapi import FastAPI
from app.api.v1.servers import router as servers_router

app = FastAPI()

# Include the routers
app.include_router(servers_router, prefix="/api/v1/servers", tags=["servers"])


@app.get("/")
def read_root():
    return {"Hello": "World"}
