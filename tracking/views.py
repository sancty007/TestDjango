from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets
from .models import Car
from .serializers import CarSerializer
from django.http import JsonResponse

# API principale pour les voitures
class CarViewSet(viewsets.ModelViewSet):
    queryset = Car.objects.all()
    serializer_class = CarSerializer


# Page de test pour vérifier que le projet fonctionne
def api_test_home(request):
    return JsonResponse({"message": "Le projet Car Tracking fonctionne !"})
