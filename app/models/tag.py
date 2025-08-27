from tortoise import fields, models
from tortoise.models import Model

class Tag(Model):
    tag_id = fields.IntField(pk=True)
    tag_name = fields.CharField(max_length=50, unique=True)

    # Diaries와 ManyToMany 관계
    diaries: fields.ManyToManyRelation["Diary"]  # Diary 모델이 나중에 import 되어야 함

    class Meta:
        table = "tags"