"""App settings"""

from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext

# Password Hashing
PWD_CONTEXT = CryptContext(schemes=["bcrypt"], deprecated="auto")


# JWT Configuration
SECRET_KEY = 'SECRET_KEY'
ENCODING_ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 120

# OAuth2 PasswordBearer for token retrieval
OAUTH2_SCHEME = OAuth2PasswordBearer(tokenUrl="token")
