from django.db import models

# Create your models here.
class FaucetModel(models.Model):
    UNPAID = 0
    PAID = 1

    STATUS_CHOICES = [
        (UNPAID, 'Unpaid'),
        (PAID, 'Paid')
    ]
    user_twitter_id = models.CharField(max_length=32)
    account_number = models.CharField(max_length=64)
    amount = models.IntegerField()
    status = models.IntegerField(choices=STATUS_CHOICES, default=UNPAID)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.account_number}: {self.amount} - {self.status}'


class Statistic(models.Model):

    total_payments = models.IntegerField(default=0)
    total_tnbc_paid = models.IntegerField(default=0)
    average_tnbc_paid = models.IntegerField(default=0)
    amount_paid_in_usd = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.total_payments} - {self.total_tnbc_paid} - {self.average_tnbc_paid}'
