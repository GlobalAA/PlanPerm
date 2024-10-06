import ast

from aiogram import F
from aiogram.types import CallbackQuery

from database.models import PermissionList
from keyboards.select import get_settings_keyboard

from . import router


@router.callback_query(F.data.startswith("change_"))
async def change_select(callback: CallbackQuery):
	_, id, selected = callback.data.split("_")

	selected: list[int] = ast.literal_eval(selected)
	if int(id) in selected:
		selected.remove(int(id))
	else:
		selected.append(int(id))

	await callback.message.edit_reply_markup(
		reply_markup=get_settings_keyboard(selected)
	)

@router.callback_query(F.data.startswith("save_"))
async def save_select(callback: CallbackQuery):
	_, selected = callback.data.split("_")

	selected: list[int] = ast.literal_eval(selected)

	send_message = 1 in selected
	send_media = 2 in selected
	add_members = 3 in selected

	try:
		if (data := await PermissionList.get_or_none(group_id = callback.message.chat.id)) != None:
			data.send_message = send_message
			data.send_media = send_media
			data.add_members = add_members
			await data.save()
		else:
			await PermissionList.create(
				group_id=callback.message.chat.id,
				send_message=send_message,
				send_media=send_media,
				add_members=add_members
			)

		await callback.message.edit_text(
			"Налаштування збережено"
		)
	except Exception as e:
		await callback.message.edit_text(
			"Сталася помилка, спробуйте ще раз"
		)
		raise(e)