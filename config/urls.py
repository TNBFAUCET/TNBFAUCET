from django.contrib import admin
from django.urls import path, include

from rest_framework.routers import DefaultRouter

from payments.urls import router as payments_router

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('payments.urls'))
]

router = DefaultRouter(trailing_slash=False)
router.registry.extend(payments_router.registry)
urlpatterns += router.urls
