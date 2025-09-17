from django.db import models

class Car(models.Model):
    license_plate = models.CharField(max_length=20)
    model = models.CharField(max_length=50)
    location = models.CharField(max_length=100)
    last_update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.model} - {self.license_plate}"
