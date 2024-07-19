# admin.py
from django.contrib import admin
from .models import Reservation

@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'date', 'time')
    list_filter = ('date', 'time')
    search_fields = ('name', 'phone')
