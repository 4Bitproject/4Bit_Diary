# app/models/diary.py

import enum

from tortoise import fields, models

# NOTE: User 모델을 직접 임포트하지 않아도 됩니다.
# from .user import User


class EmotionalState(enum.Enum):
    JOY = "기쁨"
    SAD = "슬픔"
    DEPRESSED = "우울함"
    ANGRY = "분노"


class Diary(models.Model):
    diary_id = fields.IntField(pk=True)
    # NOTE: ForeignKeyField의 첫 번째 인수를 'app_name.ModelName' 형식으로 유지합니다.
    user = fields.ForeignKeyField("models.User", related_name="diaries")
    title = fields.CharField(max_length=30, null=False)
    content = fields.CharField(max_length=100)
    emotional_summary = fields.CharField(max_length=20, null=True)
    emotional_state = fields.CharEnumField(EmotionalState)
    created_date = fields.DatetimeField(auto_now_add=True)
    updated_date = fields.DatetimeField(auto_now=True)

    def __str__(self):
        return self.title
