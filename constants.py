import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import SimpleEventIsolation
from tortoise import Tortoise

from config import config

bot = Bot(
	config.BOT_TOKEN.get_secret_value(),
	default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)
dp = Dispatcher(events_isolation=SimpleEventIsolation())

async def tortoise_init():
	await Tortoise.init(
		db_url="sqlite://db.sqlite3",
		modules={'models': ['database.models']}
	)

	await Tortoise.generate_schemas()
	logging.info("Tortoise ORM initialized")