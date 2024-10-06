from tortoise import fields, models


class PermissionList(models.Model):
	id = fields.IntField(pk=True)
	group_id = fields.BigIntField(unique=True)

	send_message = fields.BooleanField(default=True)
	send_media = fields.BooleanField(default=True)
	add_members = fields.BooleanField(default=True)

	updated_at = fields.DatetimeField(auto_now=True)
	created_at = fields.DatetimeField(auto_now_add=True)

class Users(models.Model):
	id = fields.IntField(pk=True)
	perm = fields.ForeignKeyField('models.PermissionList', related_name='users', on_delete=fields.CASCADE)
	user_id = fields.BigIntField()