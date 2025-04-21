from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.database.db_helper import db_helper
from app.database.models import Base
from users.views import router as user_router
from financial_records.views import router as financial_records_router
import uvicorn


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with db_helper.engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield


app = FastAPI(lifespan=lifespan)

app.include_router(user_router)
app.include_router(financial_records_router)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
