import asyncio
import logging
from datetime import datetime, timedelta
from typing import List

from aiogram.types import ChatPermissions
from celery import Celery
from celery.schedules import crontab
from tortoise import Tortoise

from config import config
from constants import bot, tortoise_init
from database.models import PermissionList, Users

app: Celery = Celery(
	"permissions", 
	broker="redis://localhost:6379/0",
	backend="redis://localhost:6379/1",
)

app.conf.timezone = 'Europe/Kiev'

logging.basicConfig(level=logging.INFO)

@app.task
def test_task():
	async def fetch():
		await tortoise_init()

		records = await PermissionList.all().prefetch_related("users")
		time = datetime.now() + timedelta(hours=10)

		msg = config.PERMISSION_MESSAGE.format(time=time.strftime("%H:%M"))
		for permission in records:
			users: List[Users] = await permission.users.all()
		
			for user in users:
				logging.info(permission.send_message)	
				await bot.restrict_chat_member(
					chat_id=permission.group_id,
					user_id=user.user_id,
					permissions=ChatPermissions(
						can_send_messages=permission.send_message,
						can_send_audios=permission.send_media,
						can_send_documents=permission.send_media,
						can_send_photos=permission.send_media,
						can_send_videos=permission.send_media,
						can_send_other_messages=permission.send_message,
						can_send_polls=permission.send_media,
						can_send_other_media=permission.send_media,
						can_invite_users=permission.add_members,
						can_change_info=True,
						can_pin_messages=True,
						can_manage_topics=True
					),
					until_date=time
				)

			await bot.send_message(chat_id=permission.group_id, text=msg)

		logging.info("Permissions updated")
		await Tortoise.close_connections()
	
	loop = asyncio.get_event_loop()
	loop.run_until_complete(fetch())

@app.on_after_configure.connect
def setup_periodic(sender, **kwargs):	
	sender.add_periodic_task(
		crontab(hour="23", minute="0"),
		test_task.s(),
		name="test_task"
	)