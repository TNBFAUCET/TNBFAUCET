from django.contrib import admin
from .models import Payment, Statistic, BackupStatistic

# Register your models here.
admin.site.register(Payment)
admin.site.register(Statistic)
admin.site.register(BackupStatistic)
