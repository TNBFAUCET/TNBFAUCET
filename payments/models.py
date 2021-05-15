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

    def __str__(self):
        return f'{self.account_number}: {self.amount} - {self.status}'
