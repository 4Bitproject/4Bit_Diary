from tortoise import fields, models
from tortoise.contrib.pydantic import pydantic_model_creator
from enum import Enum

class EmotionalState(str, Enum):
    HAPPY = "happy"
    SAD = "sad"
    ANGRY = "angry"
    NEUTRAL = "neutral"

class Diary(models.Model):
    id = fields.IntField(primary_key=True)
    user_id = fields.IntField()
    title = fields.CharField(max_length=100)
    content = fields.TextField()
    emotional_state = fields.CharEnumField(EmotionalState)
    ai_summary = fields.TextField(null=True)
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)

# Pydantic schemas
Diary_Pydantic = pydantic_model_creator(Diary, name="Diary")
DiaryIn_Pydantic = pydantic_model_creator(Diary, name="DiaryIn", exclude_readonly=True)
