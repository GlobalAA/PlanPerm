from typing import List

from aiogram import F
from aiogram.types import Message, User

from database.models import PermissionList, Users

from . import group


@group.message(F.new_chat_members)
async def on_join(message: Message):
	new_users: List[User] = message.new_chat_members
	perm_instance = await PermissionList.get_or_none(group_id=message.chat.id)

	if not perm_instance:
		perm_instance = await PermissionList.create(group_id=message.chat.id)

	for user in new_users:
		await Users.create(user_id=user.id, perm=perm_instance)

@group.message(F.left_chat_member)
async def on_left(message: Message):
	left_user: User = message.left_chat_member
	if left_user:
		await Users.filter(user_id=left_user.id).delete()