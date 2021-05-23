import requests

from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save


class Payment(models.Model):
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


class BackupStatistic(models.Model):

    total_payments = models.IntegerField(default=0)
    total_tnbc_paid = models.IntegerField(default=0)
    average_tnbc_paid = models.IntegerField(default=0)
    amount_paid_in_usd = models.BigIntegerField(default=0)

    def __str__(self):
        return f'{self.total_payments} - {self.total_tnbc_paid} - {self.average_tnbc_paid}'


@receiver(post_save, sender=Payment)
def save_statistics(sender, instance, created, **kwargs):
    STATS_API = "https://tnbcrow.pythonanywhere.com/statistics"
    
    if created:

        stat = Statistic.objects.first()
        
        stat.total_payments += 1
        stat.total_tnbc_paid += instance.amount
        stat.average_tnbc_paid = stat.total_tnbc_paid / stat.total_payments

        r = requests.get(STATS_API).json()

        rate_info = r['results']

        for rate in rate_info:
            last_rate = rate['last_rate']

        stat.amount_paid_in_usd += int(last_rate) * instance.amount
        
        BackupStatistic.objects.create(total_payments = stat.total_payments,
                                       total_tnbc_paid = stat.total_tnbc_paid,
                                       average_tnbc_paid = stat.average_tnbc_paid,
                                       amount_paid_in_usd = stat.amount_paid_in_usd,
                                       )
        stat.save()
