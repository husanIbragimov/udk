from tortoise import fields
from tortoise.models import Model


class Payment(Model):
    id = fields.IntField(pk=True)
    order = fields.ForeignKeyField("models.Order", related_name="payments")
    amount = fields.FloatField(null=True)
    check_image = fields.CharField(max_length=500, null=True)
    is_paid = fields.BooleanField(default=False)
    created_at = fields.DatetimeField(auto_now_add=True)

    class Meta:
        table = "payments"
        ordering = ["-id"]
