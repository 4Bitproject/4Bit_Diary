from tortoise import fields
from tortoise.models import Model


class User(Model):
    id = fields.IntField(primary_key=True)
    email = fields.CharField(max_length=255, unique=True)
    password = fields.CharField(max_length=255)
    nickname = fields.CharField(max_length=50)
    name = fields.CharField(max_length=50)
    phone_number = fields.CharField(max_length=20, null=True)
    last_login = fields.DatetimeField(null=True)
    is_staff = fields.BooleanField(default=False)
    is_admin = fields.BooleanField(default=False)
    is_active = fields.BooleanField(default=True)
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)

    def __str__(self):
        return f"{self.nickname}({self.name})"
