from fastapi import FastAPI, Path
from users.views import router as user_router
import uvicorn

app = FastAPI()

app.include_router(user_router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
