from aiogram.filters import Command
from aiogram.types import Message

from database.models import PermissionList
from filters import ChatType
from keyboards.select import get_settings_keyboard

from . import group


@group.message(Command("settings"), ChatType(["group", "supergroup"]))
async def settings(message: Message):
	global selected
	selected = []

	if (data := await PermissionList.get_or_none(group_id = message.chat.id)) != None:
		selected = [idx+1 for idx, value in enumerate([data.send_message, data.send_media, data.add_members]) if value]

	await message.answer("Виберіть права, які треба буде забирати", reply_markup=get_settings_keyboard(selected))