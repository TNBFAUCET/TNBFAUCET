from django.shortcuts import render
from django.contrib import messages
from django.views import generic
from django.contrib.auth.mixins import UserPassesTestMixin

from ..models import FaucetModel, Statistic


class Home(generic.ListView):
    template_name = 'home.html'

    def get_queryset(self):
        payments = FaucetModel.objects.all().order_by('-created_at')[:8]
        stats = Statistic.objects.first()

        query_set = {
            'payments' : payments,
            'stats' : stats,
        }

        return query_set

def home(request):
    return render(request, "index.html")

def prerequisite(request):
    return render(request, "prerequisite.html")


class PaymentIndex( UserPassesTestMixin, generic.ListView):
    template_name = "payment_index.html"

    def get_queryset(self):
        return FaucetModel.objects.order_by('status')

    def test_func(self):
        return self.request.user.is_staff