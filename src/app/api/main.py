from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.app.api.users.views import router as user_router
from src.app.api.financial_records.views import router as financial_records_router
from src.app.api.categories.views import router as categories_router
import uvicorn


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield


app = FastAPI(lifespan=lifespan, debug=True)

app.include_router(user_router)
app.include_router(financial_records_router)
app.include_router(categories_router)


if __name__ == "__main__":
    uvicorn.run(app, log_level="debug", host="0.0.0.0", port=8000)
