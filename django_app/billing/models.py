import hashlib
import random
import time

from django.contrib.auth import get_user_model
from django.db import models
from django.db.models.signals import post_save

from . import iamport

USER = get_user_model()


class Point(models.Model):
    user = models.OneToOneField(USER)
    point = models.PositiveIntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True, auto_now=False)
    timestamp = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __str(self):
        return str(self.point)


class PointTransactionManager(models.Manager):
    def create_new(self, user, amount, type, success=None, transaction_status=None):
        if not user:
            raise ValueError("유저가 확인되지 않습니다.")
        short_hash = hashlib.sha1(str(random.random()).encode()).hexdigest()[:2]
        time_hash = hashlib.sha1(str(int(time.time())).encode()).hexdigest()[-3:]
        base = str(user.email).split("@")[0]
        key = hashlib.sha1(str(short_hash + time_hash + base).encode()).hexdigest()[:10]
        new_order_id = "%s" % (key)

        iamport.validation_prepare(new_order_id, amount)

        new_trans = self.model(
            user=user,
            order_id=new_order_id,
            amount=amount,
            type=type
        )

        if success is not None:
            new_trans.success = success
            new_trans.transaction_status = transaction_status

        new_trans.save(using=self._db)
        return new_trans.order_id

    def validation_trans(self, merchant_id):
        result = iamport.get_transaction(merchant_id)

        if result['status'] is not 'paid':
            return result
        else:
            return None

    def all_for_user(self, user):
        return super(PointTransactionManager, self).filter(user=user)

    def get_recent_user(self, user, num):
        return super(PointTransactionManager, self).filter(user=user)[:num]


class PointTransaction(models.Model):
    user = models.ForeignKey(USER)
    transaction_id = models.CharField(max_length=120, null=True, blank=True)
    order_id = models.CharField(max_length=120, unique=True)
    amount = models.PositiveIntegerField(default=0)
    success = models.BooleanField(default=True)
    transaction_status = models.CharField(max_length=220, null=True, blank=True)
    type = models.CharField(max_length=120)
    created = models.DateTimeField(auto_now_add=True, auto_now=False)

    objects = PointTransactionManager()

    def __str__(self):
        return self.order_id

    class Meta:
        ordering = ['-created']


def new_point_trans_validation(sender, instance, created, *args, **kwargs):
    if instance.transaction_id:
        v_trans = PointTransaction.objects.validation_trans(
            merchant_id=instance.order_id
        )

        res_merchant_id = v_trans['merchant_id']
        res_imp_id = v_trans['imp_id']
        res_amount = v_trans['amount']

        r_trans = PointTransaction.objects.filter(
            order_id=res_merchant_id,
            transaction_id=res_imp_id,
            amount=res_amount
        ).exists()

        if not v_trans or not r_trans:
            raise ValueError("비정상적인 거래입니다.")


post_save.connect(new_point_trans_validation, sender=PointTransaction)
