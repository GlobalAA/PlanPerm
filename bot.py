import logging
from asyncio import run

from tortoise import Tortoise

from callbacks import router as callback_router
from constants import bot, dp, tortoise_init
from handlers import router

logging.basicConfig(level=logging.INFO)


@dp.startup()
async def on_startup():
	dp.include_router(router)
	dp.include_router(callback_router)
	await tortoise_init()

	await bot.delete_webhook(drop_pending_updates=True)

@dp.shutdown()
async def on_shutdown():
	await Tortoise.close_connections()

async def main():
	await dp.start_polling(bot)

if __name__ == "__main__":
	run(main())