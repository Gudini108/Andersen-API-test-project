"""Authentification endpoints"""

from fastapi.security import OAuth2PasswordRequestForm
from fastapi import APIRouter, HTTPException, status, Depends
from datetime import timedelta

from app.repo.user import UserRepo
from app.schemas import TodoUserInput
from app.settings import ACCESS_TOKEN_EXPIRE_MINUTES
from app.security import (
    get_password_hash,
    authenticate_user,
    create_access_token
)


router = APIRouter()


@router.post("/signup", tags=["Auth"])
async def signup(new_user: TodoUserInput):
    """Signup endpoint"""
    existing_user = await UserRepo.safe_get_user_by_username(new_user.username)

    if existing_user is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User with this username already exists",
        )

    new_user.password = get_password_hash(new_user.password)
    await UserRepo.save_user(new_user)
    return {"message": "Registration complete!"}


@router.post("/login", tags=["Auth"])
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    """Login endpoint"""
    user = await authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password"
        )

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username},
        expires_delta=access_token_expires
    )

    return {"access_token": access_token, "token_type": "bearer"}
