# app/models/token_blacklist.py

from tortoise import fields, models


class TokenBlacklist(models.Model):
    jti = fields.CharField(max_length=36, unique=True)
    exp = fields.DatetimeField()
