from fastapi import APIRouter

from app.api.users import crud
from app.api.users.schemas import CreateUser

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/")
def create_user(user: CreateUser):
    return crud.create_user(user_in=user)
