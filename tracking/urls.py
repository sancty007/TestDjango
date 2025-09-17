from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CarViewSet, api_test_home

router = DefaultRouter()
router.register(r'cars', CarViewSet)

urlpatterns = [
    path('', api_test_home, name='home'),  # page de test
    path('api/', include(router.urls)),    # API REST
]
