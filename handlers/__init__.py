from aiogram import Router

router = Router(name="main_router")

from .group import group
from .start import start

router.include_router(group)
