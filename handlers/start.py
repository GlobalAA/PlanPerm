from aiogram.filters import CommandStart
from aiogram.types import Message

from filters import ChatType

from . import router


@router.message(CommandStart(), ChatType("private"))
async def start(message: Message):
	await message.answer("Привіт, я можу забирати деякі права у всіх користувачів в зазначений час, додай мене, і спробуєш")