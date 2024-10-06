from aiogram import Router

group = Router(name="group_router")
from .members import on_join, on_left
from .settings import settings
