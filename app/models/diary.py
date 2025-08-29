from enum import Enum

from tortoise import fields, models
from tortoise.contrib.pydantic import pydantic_model_creator


class EmotionalState(str, Enum):
    HAPPY = "happy"
    SAD = "sad"
    ANGRY = "angry"
    NEUTRAL = "neutral"


class Diary(models.Model):
    id = fields.IntField(pk=True)
    user = fields.ForeignKeyField('models.User', related_name='diary')
    title = fields.CharField(max_length=100)
    content = fields.TextField()
    emotional_state = fields.CharEnumField(EmotionalState, null=True)
    ai_summary = fields.TextField(null=True)
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)
    tags = fields.ManyToManyField("models.Tag")


# 읽기용(응답용)
Diary_Pydantic = pydantic_model_creator(Diary, name="Diary")

# 입력용(생성/업데이트용)
DiaryIn_Pydantic = pydantic_model_creator(Diary, name="DiaryIn", exclude_readonly=True)
#
#
# class DiaryTag(models.Model):
#     diary = fields.ForeignKeyField("models.Diary", related_name="diary_tags")
#     tag = fields.ForeignKeyField("models.Tag", related_name="diary_tags")
#
#     class Meta:
#         table = "diary_tags"
#         unique_together = [("diary", "tag")]
