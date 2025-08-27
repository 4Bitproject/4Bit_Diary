from tortoise import fields, models


class Tag(models.Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=50)

    class Meta:
        table = "tag"