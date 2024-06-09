import uvicorn
from fastapi import FastAPI

from src.auth.routers import router as auth_router
from src.users.routers import router as users_router

app = FastAPI(title="JWT AUTH API")

app.include_router(users_router)
app.include_router(auth_router)

if __name__ == "__main__":
    uvicorn.run(app="main:app", reload=True, port=8000, host="0.0.0.0")
