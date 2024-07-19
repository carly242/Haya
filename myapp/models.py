from django.db import models

# Create your models here.



class Reservation(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    date = models.DateField()
    time = models.TimeField()

    def __str__(self):
        return f'{self.name} - {self.date} {self.time}'