from django.contrib import admin
from .models import FaucetModel, Statistic

# Register your models here.
admin.site.register(FaucetModel)
admin.site.register(Statistic)