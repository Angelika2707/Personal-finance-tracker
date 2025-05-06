from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.app.api.financial_records.views import router as financial_records_router
from src.app.api.categories.views import router as categories_router
import uvicorn
from src.app.api.users.views import router as user_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield


app = FastAPI(lifespan=lifespan, debug=True)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8501"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(user_router)
app.include_router(financial_records_router)
app.include_router(categories_router)


if __name__ == "__main__":
    uvicorn.run(app, log_level="debug", host="127.0.0.1", port=8000)
