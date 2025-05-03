from tortoise import fields
from tortoise.models import Model


class Order(Model):
    id = fields.IntField(pk=True)
    user = fields.ForeignKeyField("models.User", related_name="udks")
    question = fields.CharField(max_length=500, null=True)
    udk = fields.CharField(max_length=255, null=True)
    created_at = fields.DatetimeField(auto_now_add=True)
    response = fields.CharField(max_length=1000, null=True)

    class Meta:
        table = "orders"
        ordering = ["-id"]
