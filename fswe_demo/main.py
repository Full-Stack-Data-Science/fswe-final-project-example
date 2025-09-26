from fastapi import FastAPI

from fswe_demo.application.api.middleware import LoggingMiddleware
from fswe_demo.application.api.routers.item_popularity import (
    router as item_popularity_router,
)
from fswe_demo.application.api.routers.recommendations import (
    router as recommendations_router,
)

app = FastAPI(title="FSWE Demo Application")
app.add_middleware(LoggingMiddleware)
app.include_router(item_popularity_router)
app.include_router(recommendations_router)


@app.get("/")
async def root() -> dict:
    return {"message": "Hello from FSWE Demo Application!"}
