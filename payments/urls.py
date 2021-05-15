from django.urls import path, include
from .views import faucet_view, home, prerequisite

urlpatterns = [
    path('', home),
    path('add-payment/', faucet_view, name='add-payment'),
    path('prerequisite/', prerequisite, name='prerequisite')
]