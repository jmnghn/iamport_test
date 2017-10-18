from django.contrib.auth import get_user_model
from django.db import models

USER = get_user_model()


class Point(models.Model):
    user = models.OneToOneField(USER)
    point = models.PositiveIntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True, auto_now=False)
    timestamp = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __str(self):
        return str(self.point)


class PointTransaction(models.Model):
    user = models.ForeignKey(USER)
    transaction_id = models.CharField(max_length=120, null=True, blank=True)
    order_id = models.CharField(max_length=120, unique=True)
    amount = models.PositiveIntegerField(default=0)
    success = models.BooleanField(default=True)
    transaction_status = models.CharField(max_length=220, null=True, blank=True)
    type = models.CharField(max_length=120)
    created = models.DateTimeField(auto_now_add=True, auto_now=False)

    def __str__(self):
        return self.order_id

    class Meta:
        ordering = ['-created']
