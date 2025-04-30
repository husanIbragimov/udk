from tortoise import fields
from tortoise.models import Model


class Order(Model):
    id = fields.IntField(pk=True)
    user = fields.ForeignKeyField("models.User", related_name="udks")
    udk = fields.CharField(max_length=255, null=True)
    created_at = fields.DatetimeField(auto_now_add=True)

    class Meta:
        table = "orders"
        ordering = ["-id"]
