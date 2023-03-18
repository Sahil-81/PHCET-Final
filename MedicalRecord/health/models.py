from django.db import models

# Create your models here.


class PatientAddress(models.Model):
    role = models.CharField(max_length=30)
    address = models.CharField(max_length=50)


    def __str__(self):
        return self.role