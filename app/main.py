"""App startup, shutdown and root endpoints handelings"""

from fastapi import FastAPI, APIRouter
from fastapi_pagination import add_pagination
import sqlalchemy
from app.config import settings

from app.db import database, metadata
from app.routers.auth import router as auth_router
from app.routers.users import router as users_router
from app.routers.tasks import router as tasks_router


API_DESCRIPTION = """
Simple RESTful API using FastAPI for a social networking application

## Functions

* **Signup as a new user**
* **Login as a registered user and obtain JWT-token**
* **Create, Delete, Edit and View Tasks**
* **Set status to Tasks**
"""

app = FastAPI(
    title='Webtronics FastAPI test project',
    description=API_DESCRIPTION,
    version='1.0.0'
)
add_pagination(app)
router = APIRouter()


@app.get('/', tags=['Root'])
def root():
    """Root endpoint"""
    return {
        'signup': app.url_path_for('signup'),
        'login': app.url_path_for('login'),
        'users': app.url_path_for('get_all_users'),
        'tasks': app.url_path_for('get_all_user_tasks')
    }


api_prefx = '/api/v1'
app.include_router(router, prefix=api_prefx)
app.include_router(auth_router, prefix=api_prefx)
app.include_router(users_router, prefix=api_prefx)
app.include_router(tasks_router, prefix=api_prefx)


@app.on_event("startup")
async def startup():
    """Connects to DB"""
    engine = sqlalchemy.create_engine(settings.db_url)
    metadata.create_all(engine)

    if not database.is_connected:
        await database.connect()


@app.on_event("shutdown")
async def shutdown():
    """Closes all connections to DB"""
    if database.is_connected:
        await database.disconnect()
