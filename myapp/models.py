from django.db import models
from django.contrib.auth.models import User
from datetime import time as djangotime
from django.core.exceptions import ValidationError

# Create your models here.




class Reservation(models.Model):
    STATUS_CHOICES = [
        ('pending', 'En attente'),
        ('confirmed', 'Confirmée'),
        ('cancelled', 'Annulée'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reservations')
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    date = models.DateField()
    time = models.TimeField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')

    def __str__(self):
        return f"{self.name} - {self.date} {self.time}"

    def clean(self):
        # Validation pour l'heure de réservation
        opening_time = djangotime(9, 0)  # 09:00
        closing_time = djangotime(18, 0)  # 18:00

        if not (opening_time <= self.time <= closing_time):
            raise ValidationError('Les réservations ne peuvent être effectuées qu\'entre 09:00 et 18:00.')

        # Validation pour le jour de la semaine (pas de réservation le dimanche)
        if self.date.weekday() == 6:  # 6 correspond à dimanche
            raise ValidationError('Les réservations ne sont pas disponibles le dimanche.')

    class Meta:
        unique_together = ('date', 'time')
    
    
class Profile(models.Model):
        user = models.OneToOneField(User, on_delete=models.CASCADE)
        phone = models.CharField(max_length=15, blank=True)
        loyalty_points = models.IntegerField(default=0)

        def __str__(self):
            return self.user.username
   
        
from django.http import HttpResponse

        
def debug_view(request):
    user = request.user
    if user.is_authenticated:
        try:
            profile = Profile.objects.get(user=user)
            return HttpResponse(f"User profile exists for: {user.username}")
        except Profile.DoesNotExist:
            return HttpResponse("Profile does not exist.")
    return HttpResponse("User not authenticated.")