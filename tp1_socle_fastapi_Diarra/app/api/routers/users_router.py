from fastapi import APIRouter, Depends, HTTPException
from app.api.dependencies import get_users_service_dep
from app.models.user_model import UserModel
from app.models.user_model_create import UserModelCreate
from app.services.users_service import UsersService

router = APIRouter(prefix="/users", tags=["users"])

@router.get("", response_model=list[UserModel])
def list_users(service: UsersService = Depends(get_users_service_dep)) -> list[UserModel]:
    return service.list_users()

@router.get("/{user_id}", response_model=UserModel)
def get_user(user_id: int, service: UsersService = Depends(get_users_service_dep)) -> UserModel:
    user = service.get_user_by_id(user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.post("", response_model=UserModel, status_code=201)
def create_user(payload: UserModelCreate, service: UsersService = Depends(get_users_service_dep)) -> UserModel:
    return service.create_user(payload)