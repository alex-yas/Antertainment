from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from route_homepage import general_pages_router
from model.session import engine
from model.base import Base


def include_router(fast_app):
    fast_app.include_router(general_pages_router)


def configure_static(fast_app):
    fast_app.mount("/static", StaticFiles(directory="static"), name="static")


def create_tables():
    Base.metadata.create_all(bind=engine)


def start_application():
    fast_app = FastAPI()
    include_router(fast_app)
    configure_static(fast_app)
    create_tables()
    return fast_app


app = start_application()
