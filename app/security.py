"""Verifications and security"""

import jwt
import datetime
from datetime import datetime as dtime
from fastapi import HTTPException, Depends
from ormar.exceptions import NoMatch

from app.repo.user import UserRepo
from app.settings import (
    PWD_CONTEXT,
    SECRET_KEY,
    ENCODING_ALGORITHM,
    OAUTH2_SCHEME
)


def verify_password(plain_password, hashed_password):
    """Verify user password with hashed from db"""
    return PWD_CONTEXT.verify(plain_password, hashed_password)


def get_password_hash(password):
    """Hash user password"""
    return PWD_CONTEXT.hash(password)


async def authenticate_user(username: str, password: str):
    """Authenticate user with password verification"""
    user = await UserRepo.safe_get_user_by_username(username=username)
    if user and verify_password(password, user.password):
        return user
    return None


def create_access_token(data: dict, expires_delta: datetime.timedelta):
    """Generates a JWT-access-token"""
    encode_data = data.copy()
    expire_time = dtime.utcnow() + expires_delta
    encode_data.update({'exp': expire_time})
    encoded_jwt = jwt.encode(
        encode_data,
        key=SECRET_KEY,
        algorithm=ENCODING_ALGORITHM
    )
    return encoded_jwt


def verify_token(token: str = Depends(OAUTH2_SCHEME)):
    """Verify JWT-token"""
    try:
        payload = jwt.decode(token, SECRET_KEY,
                             algorithms=[ENCODING_ALGORITHM])
        return payload

    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail='Token has expired')

    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail='Invalid token')


async def get_current_user(token_payload: dict = Depends(verify_token)):
    """Takes JWT-token from payload and returns current user"""
    username: str = token_payload.get('sub')

    if username is None:
        raise HTTPException(status_code=401,
                            detail='Invalid authentication credentials')

    try:
        user = await UserRepo.safe_get_user_by_username(username=username)
        return user

    except NoMatch:
        raise HTTPException(
            status_code=401,
            detail="User not found"
        )
