from django.db import models
from django.utils.translation import gettext_lazy as _


class PaymentStatus(models.IntegerChoices):
    pending = 1, _("Pending")
    success = 2, _("Successful")
    faild = 3, _("Failed")


class PaymentModel(models.Model):
    authority = models.CharField(max_length=40)
    amount = models.DecimalField(decimal_places=0, max_digits=10)
    order = models.ForeignKey(
        "order.OrderModel",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="order_model",
    )
    status = models.IntegerField(
        choices=PaymentStatus.choices, default=PaymentStatus.pending.value
    )

    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.authority} , {self.amount}"
