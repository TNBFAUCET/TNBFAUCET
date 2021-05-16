from django.urls import path, include
from .views.parsing import faucet_view
from .views.views import Home, prerequisite, PaymentIndex

urlpatterns = [
    path('', Home.as_view()),
    path('add-payment/', faucet_view, name='add-payment'),
    path('prerequisite/', prerequisite, name='prerequisite'),
    path('payments/', PaymentIndex.as_view())
]
