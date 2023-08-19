from fastapi.security import OAuth2PasswordRequestForm
from fastapi import APIRouter, HTTPException, status, Depends
from ormar.exceptions import NoMatch
from datetime import timedelta

from app.db import TodoUser
from app.settings import ACCESS_TOKEN_EXPIRE_MINUTES
from app.security import (
    get_password_hash,
    authenticate_user,
    create_access_token
)


router = APIRouter()


@router.post("/signup", tags=["Auth"])
async def signup(user: TodoUser):
    """Signup endpoint"""
    try:
        username_exists = await (
            TodoUser.objects.filter(username=user.username).first())

        if username_exists:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User with this username already exists",
            )
    except NoMatch:
        pass

    user.password = get_password_hash(user.password)
    await user.save()
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
