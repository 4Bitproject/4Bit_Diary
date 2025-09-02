from enum import Enum

from tortoise import fields, models


class EmotionalState(str, Enum):
    HAPPY = "happy"
    SAD = "sad"
    ANGRY = "angry"
    NEUTRAL = "neutral"


class Diary(models.Model):
    id = fields.IntField(primary_key=True)
    user = fields.ForeignKeyField("models.User", related_name="diary")
    title = fields.CharField(max_length=100)
    content = fields.TextField()
    emotional_state = fields.CharEnumField(EmotionalState, null=True)
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)
    tags = fields.ManyToManyField("models.Tag")
    # ai_summary = fields.TextField()


class DiaryTag(models.Model):
    diary = fields.ForeignKeyField("models.Diary", related_name="diary_tags")
    tag = fields.ForeignKeyField("models.Tag", related_name="diary_tags")

    class Meta:
        table = "diary_tags"
        unique_together = [("diary", "tag")]
